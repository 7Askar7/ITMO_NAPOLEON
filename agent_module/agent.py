from prompts import PROMPT_CLASSIFICATION, PROMPT_DIALOGUE, PROMPT_DETECTION, PROMT_QUESTION_COMPANY, PROMPT_FOR_GENERATION 
from Gigachat import GigaChatBOT
from db.db_request import send_query
from llm_request import send_request_choco
from messages import MES_1, MES_2
import os
import sys
from mail_script import send_email
import random

class AgentBot:

    def __init__(self) -> None:
        self.gigachat = GigaChatBOT()

    def check_coffe_dialog(self, answer):
        get_answer = {"да": 0, "нет": 0} 

        for i in range(3):  # Iterating three times to check
            topic = self.gigachat.query_text(PROMPT_CLASSIFICATION, answer)
            if "да" in topic.lower():
                get_answer["да"] += 1
            else:
                get_answer["нет"] += 1

        return "да" if get_answer["да"] > get_answer["нет"] else "нет"

    def check_dialog_continue(self, answer):
        get_answer_dialog = {"да": 0, "нет": 0} 

        for i in range(3):
            topic_dialog = self.gigachat.query_text(PROMPT_DIALOGUE, answer)
            if "да" in topic_dialog.lower():
                get_answer_dialog["да"] += 1
            else:
                get_answer_dialog["нет"] += 1

        return "да" if get_answer_dialog["да"] > get_answer_dialog["нет"] else "нет"

    def retrieve_contact(self, answer):
        get_answer_contact = {"contact": 0, "нет": 0} 

        for i in range(3):
            contact = self.gigachat.query_text(PROMPT_DETECTION, answer)
            if "нет" in contact.lower():
                get_answer_contact["нет"] += 1
            else:
                get_answer_contact["contact"] += 1

        if get_answer_contact["contact"] > get_answer_contact["нет"]:
            try:
                print(contact)
                return contact.split(":")[1] # Assumes contact details follow "contact: ..."
            except IndexError:
                return "нет"
        return "нет"
    
    def question_about_company(self,answer):

        get_company_answer = {"да": 0, "нет": 0} 

        for i in range(3):
            topic_dialog = self.gigachat.query_text(PROMT_QUESTION_COMPANY, answer)
            if "да" in topic_dialog.lower():
                get_company_answer["да"] += 1
            else:
                get_company_answer["нет"] += 1

        return "да" if get_company_answer["да"] > get_company_answer["нет"] else "нет"


    def start_message_with_user_email(self, user: str, file = None):
        randoms = [MES_1, MES_2]
        selected_item = random.choice(randoms)
        send_to_uswer = send_email(user, selected_item, file)

        return "Письмо отправлено!"


    def scenario(self, answer):
        coffi_dialog = self.check_coffe_dialog(answer)

        if coffi_dialog == "да":
            retr = send_query(answer, 5)
            USER_PROMPT = f"""Запрос пользователя про кофе: {answer}
                            Отзывы: {retr}"""
            otvet = GigaChatBOT().query_text(PROMPT_FOR_GENERATION, USER_PROMPT)
            return otvet
        else:
            dialog_continue = self.check_dialog_continue(answer)
            contact = self.retrieve_contact(answer)

            if dialog_continue.lower() == "да" and contact !=  "нет":
                return self.start_message_with_user_email(contact)
            
            elif dialog_continue == "нет" and contact !=  "нет":
                return self.start_message_with_user_email(contact)
            
            elif dialog_continue == "да" and contact ==  "нет":
                    return """Если у Вас вопросы по компании, то напишите пожалуйста сюда info@napoleonit.ru"""

            elif dialog_continue == "нет" and contact ==  "нет":
                return f"Извините, пока"
            
    

