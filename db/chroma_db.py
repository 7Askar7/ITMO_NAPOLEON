import chromadb
from chromadb.utils import embedding_functions
import pandas as pd


def create_db(dir_name: str):
    '''
    Функция для создания векторной бд

    Args:
        dir_name (str): путь к папке с бд
    '''
    df = pd.read_excel('Tasty_cofee_data.xlsx', engine='openpyxl', index_col = 0)
    buf = df[~df['Product Name'].isna()].drop_duplicates(subset=['Review Text', 'Sentiment'])
    chroma_client = chromadb.PersistentClient(path=dir_name)
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-large")
    collection = chroma_client.get_or_create_collection(name="hack", embedding_function=sentence_transformer_ef)
    ids = []
    id = 1
    metadatas = []
    texts = []
    for i, row in buf.iterrows():
        texts.append(row['Review Text'])
        metadatas.append({'Product Name': row['Product Name'],
                        'Sentiment': row['Sentiment'],
                        'Marketplace': row['Marketplace']})
        ids.append(str(id))
        id+=1
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )


def get_data(dir_name: str, prompt: str):
    '''
    Функция извлечения данных из векторной бд

    Args:
        dir_name (str): путь к папке с бд
        prompt (_type_): текст, к которому надо найти ближайший

    Returns:
        results: результат поиска совпадений
    '''
    chroma_client = chromadb.PersistentClient(path=dir_name)
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-large")
    collection = chroma_client.get_or_create_collection(name="hack", embedding_function=sentence_transformer_ef)
    results = collection.query(
        query_texts=[prompt],
        n_results=5,
        include=['documents', 'distances', 'metadatas']
    )
    return results