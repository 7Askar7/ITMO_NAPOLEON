from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import logging
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

app = FastAPI()

class QueryRequest(BaseModel):
    query_text: str
    n_results: int = 5

class RetrievalQuery:
    """
    Класс для выполнения запросов к коллекции Chromadb.
    """
    def __init__(self, client_path, model_name, collection_name, log_file='app.log'):
        """
        Инициализирует клиента Chromadb и эмбеддер, создает коллекцию.
        """
        self.client_path = client_path
        self.model_name = model_name
        self.collection_name = collection_name

        # Настройка логирования
        logging.basicConfig(filename=log_file, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

        # Инициализация клиента и функции эмбеддинга
        self.client = PersistentClient(path=self.client_path)
        self.sentence_transformer_ef = SentenceTransformerEmbeddingFunction(model_name=self.model_name)
        self.col = self.client.get_or_create_collection(name=self.collection_name, embedding_function=self.sentence_transformer_ef, metadata={"hnsw:space": "cosine"})

    def query_collection(self, query_text, n_results=5):
        """
        Выполняет запрос к коллекции и возвращает результаты.
        """
        try:
            results = self.col.query(
                query_texts=[query_text],
                n_results=n_results,
                include=['documents', 'distances', 'metadatas']
            )
            return results
        except Exception as e:
            print(e)
            logging.error("Error occurred", exc_info=True)
            return None

    def print_results(self, results):
        """
        Печатает результаты запроса, включая documents, distances, metadatas.
        """
        doc_results = results.get('documents', [])[0]
        print("Documents:")
        for doc_res in doc_results:
            print(doc_res)
        return doc_results

# Инициализация клиента
client_path = "DB\\vector_hack"
model_name = "intfloat/multilingual-e5-large"
collection_name = "hack"

retrieval_query = RetrievalQuery(client_path, model_name, collection_name)

@app.post("/query/")
async def query_database(query_request: QueryRequest):
    """
    Обрабатывает запрос и возвращает результаты из коллекции.
    """
    query_text = query_request.query_text
    n_results = query_request.n_results
    results = retrieval_query.query_collection(query_text, n_results)
    if results:
        doc_results = retrieval_query.print_results(results)
        return {"documents": doc_results}
    else:
        return {"error": "Query failed"}

# Запуск сервера через uvicorn и создание Ngrok туннеля
if __name__ == "__main__":
    import uvicorn

    # Запуск uvicorn с указанным хостом и портом
    uvicorn.run(app, host="0.0.0.0", port=8008)
