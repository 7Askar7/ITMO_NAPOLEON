import requests
import logging

logger = logging.getLogger(__name__)

# Публичный URL FastAPI приложения через Ngrok
url = "https://8713-93-175-29-74.ngrok-free.app/generate/"

def send_request_choco(PROMPT, USER):
    """
    Отправляет запрос к FastAPI серверу с указанным промптом и пользователем.

    :param PROMPT: Системный промпт для модели.
    :param USER: Вопрос пользователя.
    :return: Сгенерированный текст от модели.
    """
    # Данные запроса (prompt) с ролями и контентом
    data = {
        "prompt": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": USER}
        ]
    }

    try:
        # Логируем отправку запроса
        logger.info(f"Отправляем запрос с PROMPT: '{PROMPT}' и USER: '{USER}'")

        # Отправляем POST-запрос
        response = requests.post(url, json=data)

        # Проверяем статус ответа
        if response.status_code == 200:
            generated_text = response.json().get("generated_text", "")
            logger.info(f"Сгенерированный текст: {generated_text}")
            return generated_text
        else:
            error_message = f"Ошибка: {response.status_code} - {response.text}"
            logger.error(error_message)
            return error_message

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при выполнении запроса: {e}", exc_info=True)
        return f"Ошибка при выполнении запроса: {str(e)}"

if __name__ == "__main__":
    result = send_request("Ты отвечаешь на вопросы", "Кто такой Обама?")
    print(result)