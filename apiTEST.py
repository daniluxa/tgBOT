import requests
import time

URL = 'https://api.telegram.org/bot'
TOKEN = '6331123145:AAGRs5H8RS0TJaXiZ7Y44wuvsn9kKzOV1AE'
CHAT_ID = '495383721'
TEXT = 'опа плюс 1'
MAX_COUNTER = 100

offset = -2
counter = 0
chat_id: int

while counter < MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет

    updates = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')

    time.sleep(1)
    counter += 1
