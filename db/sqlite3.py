import pandas as pd
import sqlite3

def create_db(path_to_db: str):
    '''
    Функция для создания бд

    Args:
        path_to_db (str): путь к папке с бд
    '''
    conn =  sqlite3.connect(path_to_db)
    # Создаем объект типа cursor для доступа к данным
    cursor = conn.cursor()
    df = pd.read_excel('Tasty_cofee_data.xlsx', engine='openpyxl', index_col = 0)
    buf = df[~df['Product Name'].isna()].drop_duplicates(subset=['Review Text', 'Sentiment'])
    buf.to_sql('info', con = conn)
    # Подтверждаем изменения (обязательно)
    conn.commit()
    print(cursor.execute('select * from info').fetchall())
    # Закрываем курсор
    cursor.close()
    # Закрываем соединение (рекомендуется)
    conn.close()
    
    
def get_data(path_to_db: str):
    '''
    Функция извлечения данных из бд

    Args:
        path_to_db (str): путь к папке с бд

    Returns:
        res: результат выгрузки данных
    '''
    conn =  sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    res = pd.read_sql('select * from info', con = conn)
    cursor.close()
    conn.close()
    return res