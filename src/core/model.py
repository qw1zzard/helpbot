from functools import lru_cache

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_qdrant import Qdrant
from more_itertools import chunked
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from src.core.history import ChatHistoryStore
from src.core.settings import Settings, get_settings


def get_vectorstore(settings: Settings) -> Qdrant:
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embed_model_name,
        model_kwargs={'device': settings.device},
    )
    client = QdrantClient(url=settings.qdrant_url)
    collection_name = settings.collection_name

    if collection_name not in [c.name for c in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=len(embeddings.embed_query('test')),
                distance=Distance.COSINE,
            ),
        )

    vectorstore = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )

    if client.count(collection_name=collection_name).count == 0:
        loader = CSVLoader(
            file_path=settings.csv_name,
            metadata_columns=['id'],
            content_columns=['question', 'answer'],
            encoding='utf-8',
        )
        for chunk in chunked(loader.load(), 3000):
            vectorstore.add_documents(documents=chunk)

    return vectorstore


def get_chat_prompt(prompt: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ('system', prompt),
            MessagesPlaceholder('history'),
            ('human', '{input}'),
        ]
    )


def create_conversational_rag_chain() -> RunnableWithMessageHistory:
    settings = get_settings()

    llm = ChatOllama(
        model=settings.chat_model_name,
        temperature=settings.temperature,
        base_url='http://ollama:11434/',
    )

    vectorstore = get_vectorstore(settings)

    retriever = vectorstore.as_retriever(
        search_type=settings.search_type,
        search_kwargs={
            'k': settings.num_answers,
            'lambda_mult': settings.lambda_mult,
        },
    )

    context_prompt = get_chat_prompt(settings.context_prompt)
    qa_prompt = get_chat_prompt(settings.system_prompt)

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, context_prompt
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    history_store = ChatHistoryStore()

    return RunnableWithMessageHistory(
        rag_chain,
        lambda session_id: history_store.get_history(session_id),
        input_messages_key='input',
        history_messages_key='history',
        output_messages_key='answer',
    )


@lru_cache
def get_chain() -> RunnableWithMessageHistory:
    return create_conversational_rag_chain()


def get_rag_answer(session_id: str, user_input: str) -> str:
    response = get_chain().invoke(
        {'input': user_input},
        config={'configurable': {'session_id': session_id}},
    )
    return response['answer']
