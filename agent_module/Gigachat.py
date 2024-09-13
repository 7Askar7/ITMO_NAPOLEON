from langchain_community.chat_models import GigaChat
from langchain.schema import HumanMessage, SystemMessage

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings import CREDENTIAL


class GigaChatBOT:

    def __init__(self) -> None:
        self.CREDENTIAL = CREDENTIAL
        self.model = self.init_gigachat()

    def init_gigachat(self):

        gigachat = GigaChat(
            credentials=self.CREDENTIAL,
            scope="GIGACHAT_API_CORP",
            model="GigaChat-Pro",
            verify_ssl_certs=False
        )

        return gigachat


    def query_text(self, system_prompt: str, user_message: str) -> str:

        messages = [
            SystemMessage(content= system_prompt),
            HumanMessage(content=f"""{user_message}""")
        ]

        answer = self.model.invoke(messages)

        return answer.content
    
if __name__ == "__main__":
    giga_chat = GigaChatBOT()
    print(GigaChatBOT().query_text(giga_chat,))