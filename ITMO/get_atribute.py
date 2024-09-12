from DB.loader import get_data
from Agent.Gigachat import GigaChatBOT
import json
import os 

class GetAttribute:

    def __init__(self) -> None:
        self.coffe_data = get_data()
        self.gigachat = GigaChatBOT().init_gigachat()

    def generator(self):

        topics = self.coffe_data["Topic"].unique()

        PROMPT_START = f"""
            Для каждого атрибута из списка напиши краткое описание, используя только отзывы пользователей. 
            Не добавляй собственную информацию и не изменяй суть сказанного. Оформляй только на основе того, что указано в отзывах.
            Если отзыв не содержит информации по какому-то атрибуту, напиши 'Нет значения'.
            Формат ответа:
            Категория: Описание (до 5 слов).

            АТРИБУТЫ:
            {topics}
            """

        FINALL_PROMPT = """
            Сформируй итоговый ответ на основе переданных данных. 
            Описание каждого атрибута должно быть кратким и основываться исключительно на предоставленных данных. 
            Если атрибут не имеет описания, оставь пометку 'Нет значения'.
            Формат ответа:
            Категория: Описание.
            """

        itog = {}
        product_name = list(set(list(self.coffe_data["Product Name"])))

        for name in product_name[:3]:
            review_on_name = list(self.coffe_data[self.coffe_data["Product Name"] == name]["Review Text"])[:90]
            result = ""

            for review in range(0,len(review_on_name), 30):
                answer = GigaChatBOT().query_text(self.gigachat, review_on_name[review:review+30], PROMPT_START)
                result += answer + "\n"
            
            finall_answer = GigaChatBOT().query_text(self.gigachat, result, FINALL_PROMPT)
            itog[name] = finall_answer

        # Сохранение результата в JSON файл
        json_file_path = "itog_results.json"
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(itog, json_file, ensure_ascii=False, indent=4)  # ensure_ascii=False сохраняет кириллицу корректно

        print(f"Результаты сохранены в {json_file_path}")

        # Возвращаем абсолютный путь к файлу
        return os.path.abspath(json_file_path)