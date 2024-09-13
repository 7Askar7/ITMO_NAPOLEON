import requests
import logging

logger = logging.getLogger(__name__)

def send_query(query_text, n_results=5):
    """
    Отправляет POST-запрос на FastAPI сервер с запросом к коллекции.

    :param query_text: Текст для запроса в коллекцию.
    :param n_results: Количество возвращаемых результатов (по умолчанию 3).
    :return: Результаты запроса или сообщение об ошибке.
    """
    # URL FastAPI приложения
    url = "http://127.0.0.1:8008/query/"

    # Данные запроса
    data = {
        "query_text": query_text,
        "n_results": n_results
    }

    try:
        # Логируем отправку запроса
        logging.info(f"Отправляем запрос: {query_text}")

        # Отправляем POST-запрос
        response = requests.post(url, json=data)

        # Проверяем статус ответа
        if response.status_code == 200:
            documents = response.json().get("documents", [])
            logging.info(f"Получены документы: {documents}")
            return documents
        else:
            error_message = f"Error: {response.status_code} - {response.text}"
            logging.error(error_message)
            return error_message

    except Exception as e:
        logging.error(f"Ошибка при выполнении запроса: {e}", exc_info=True)
        return str(e)

# Пример использования функции
if __name__ == "__main__":
    result = send_query("Расскажи мне про Дрип кофе Tasty Coffee Бэрри, positive", n_results=3)
    print(result)