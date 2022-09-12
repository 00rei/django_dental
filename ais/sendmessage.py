import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def sendTelegram(fio, phone, text):
    api = 'https://api.telegram.org/bot'
    method = api + os.environ.get('token') + '/sendMessage'
    text = f"*Новая заявка*\n\n" \
           f"ФИО — _{fio}_\n" \
           f"Текст заявки:\n" \
           f"_{text}_\n\n" \
           f"Телефон — `{phone}`"
    req = requests.post(method, data={
        'chat_id': os.environ.get('chat_id'),
        'text': text,
        'parse_mode': 'markdown'
    })
