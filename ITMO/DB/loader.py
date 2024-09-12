import sqlite3
import pandas as pd
import pandas as pd

def get_data():
    # Подключаемся к базе данных
    conn = sqlite3.connect('DB\\hack.db')

    # Создаем курсор
    cursor = conn.cursor()

    # Выполняем запрос и загружаем данные в DataFrame
    res = pd.read_sql('select * from info', con=conn)

    # Закрываем соединение
    conn.close()

    coffe_data = pd.DataFrame(res)

    return coffe_data