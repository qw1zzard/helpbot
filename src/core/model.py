from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import CSVLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_qdrant import Qdrant
from more_itertools import chunked
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from src.core.settings import Settings


def get_chat_prompt(prompt: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ('system', prompt),
            MessagesPlaceholder('history'),
            ('human', '{input}'),
        ]
    )


_global_store: dict[str, ChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in _global_store:
        _global_store[session_id] = ChatMessageHistory()
    return _global_store[session_id]


def create_conversational_rag_chain() -> RunnableWithMessageHistory:
    settings = Settings()  # type: ignore

    llm = ChatOllama(
        model=settings.chat_model_name,
        temperature=settings.temperature,
        base_url='http://ollama:11434/',
    )

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embed_model_name,
        model_kwargs={'device': settings.device},
    )

    qdrant_client = QdrantClient(url=settings.qdrant_url)
    collection_name = settings.collection_name

    existing_collections = [c.name for c in qdrant_client.get_collections().collections]
    if collection_name not in existing_collections:
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=len(embeddings.embed_query('test')),
                distance=Distance.COSINE,
            ),
        )

    vectorstore = Qdrant(
        client=qdrant_client,
        collection_name=collection_name,
        embeddings=embeddings,
    )

    if qdrant_client.count(collection_name=collection_name).count == 0:
        loader = CSVLoader(
            file_path=settings.csv_name,
            metadata_columns=['id'],
            content_columns=['question', 'answer'],
            encoding='utf-8',
        )
        for chunk in chunked(loader.load(), 3000):
            vectorstore.add_documents(documents=chunk)

    retriever = vectorstore.as_retriever(
        search_type=settings.search_type,
        search_kwargs={
            'k': settings.num_answers,
            'lambda_mult': settings.lambda_mult,
        },
    )

    contextualize_q_prompt = get_chat_prompt(settings.contextualize_q_system_prompt)
    qa_prompt = get_chat_prompt(settings.system_prompt)

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key='input',
        history_messages_key='history',
        output_messages_key='answer',
    )


conversational_rag_chain: RunnableWithMessageHistory | None = None


def get_rag_answer(session_id: str, user_input: str) -> str:
    global conversational_rag_chain

    if conversational_rag_chain is None:
        conversational_rag_chain = create_conversational_rag_chain()

    response = conversational_rag_chain.invoke(
        {'input': user_input},
        config={'configurable': {'session_id': session_id}},
    )
    return response['answer']
