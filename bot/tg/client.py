import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse, get_updates_schema, send_message_schema


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        """
                URL метод для запроса к telegram боту
                Args:
                    method: какой запрос будет отправлен боту
                Returns:
                    str
                """
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """
                Получения входящих обновлений от пользователя.
                Args:
                    offset: int
                    timeout: int
                Returns:
                    GetUpdatesResponse
                """
        response = requests.get(self.get_url(f'getUpdates?offset={offset}&timeout={timeout}&'
                                             f"allowed_updates=['update_id','message']"))
        json_data = response.json()
        print(json_data)
        result = get_updates_schema().load(json_data)

        return result

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """
               Отправление сообщения пользователю от бота.
               Args:
                   chat_id: int
                   text: int
               Returns:
                   SendMessageResponse
               """
        response = requests.get(self.get_url(f'sendMessage?chat_id={chat_id}&text={text}'))
        json_data = response.json()
        result = send_message_schema().load(json_data)

        return result



# cl = TgClient("6187763368:AAGEiOYId1RLD3jQd-vgBeWMv5eHps33j2c")
# print(cl.get_updates(offset=0, timeout=60))
#

# cl = TgClient("6187763368:AAGEiOYId1RLD3jQd-vgBeWMv5eHps33j2c")
# print(cl.send_message(726484566, "hello"))
