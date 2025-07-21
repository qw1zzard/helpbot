import csv

import requests
from more_itertools import chunked
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer
from src.core.history import ChatHistoryStore
from src.core.settings import get_settings

settings = get_settings()
qdrant_client = QdrantClient(url=settings.qdrant_url)
collection_name = settings.collection_name
history_store = ChatHistoryStore()
embedding_model = SentenceTransformer(settings.embed_model_name)


def load_csv_documents(file_path: str) -> list[dict]:
    documents = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            doc = {
                'id': row['id'],
                'question': row['question'],
                'answer': row['answer'],
            }
            documents.append(doc)
    return documents


def recreate_collection_if_needed():
    if collection_name not in [
        c.name for c in qdrant_client.get_collections().collections
    ]:
        dim = len(embedding_model.encode('test'))
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )


def populate_if_empty():
    count = qdrant_client.count(collection_name=collection_name).count
    if count == 0:
        rows = load_csv_documents(settings.csv_name)
        points = []

        for idx, row in enumerate(rows):
            text = f'Q: {row["question"]}\nA: {row["answer"]}'
            vector = embedding_model.encode(text).tolist()
            points.append(
                PointStruct(
                    id=idx,
                    vector=vector,
                    payload={
                        'id': row['id'],
                        'answer': row['answer'],
                        'question': row['question'],
                    },
                )
            )

        for batch in chunked(points, 3000):
            qdrant_client.upsert(collection_name=collection_name, points=batch)


def get_rag_answer(session_id: str, user_input: str) -> str:
    history_store.add_message(session_id, 'user', user_input)
    history = history_store.get_history(session_id)

    query_vector = embedding_model.encode(user_input)

    search_result = qdrant_client.search(
        collection_name=settings.collection_name,
        query_vector=query_vector,  # type: ignore
        limit=settings.num_answers,
    )

    context = '\n---\n'.join(
        hit.payload.get('answer', '') for hit in search_result if hit.payload
    )

    system_prompt = settings.system_prompt
    history_messages = '\n'.join(f'{m["role"]}: {m["content"]}' for m in history)
    prompt = (
        f'{system_prompt}\n\n'
        f'Context:\n{context}\n\n'
        f'Chat History:\n{history_messages}\n\n'
        f'User: {user_input}\nAssistant:'
    )

    response = requests.post(
        'http://ollama:11434/api/chat',
        json={
            'model': settings.chat_model_name,
            'messages': [{'role': 'user', 'content': prompt}],
            'stream': False,
        },
        timeout=30,
    )
    response.raise_for_status()
    answer = response.json()['message']['content']

    history_store.add_message(session_id, 'assistant', answer)

    return answer
