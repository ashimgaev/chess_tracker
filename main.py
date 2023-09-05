
from win10toast import ToastNotifier
import csv
import requests
from bs4 import BeautifulSoup
import time

def send_toast():
    toast = ToastNotifier()
    toast.show_toast(
        "Notification",
        "Notification body",
        duration = 5,
        threaded = True,
    )

    while toast.notification_active:
        time.sleep(1)

def do_main():
    print('hello')
    BASE_URL = 'https://ratings.ruchess.ru'
    
    with open('data.csv', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            name = row[0]
            id = row[1]
            current_status = str(row[2])
            print(f'Анализ {name} ФШР ID({id}) ...')
            http_response = requests.get(f'{BASE_URL}/people/{id}')
            if http_response.status_code >= 200 and http_response.status_code < 300:
                soup = BeautifulSoup(http_response.text, features='html.parser')
                item = soup.find('strong', string='Разряд')
                if item:
                    status = item.parent.text.replace('\n', '')
                else:
                    status = 'пусто'
                print(f'    Статус: {status}')
                if str(status) != current_status:
                    send_toast()


if __name__ == '__main__':
    do_main()