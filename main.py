
from win10toast import ToastNotifier
import csv
import requests
from bs4 import BeautifulSoup
import time

DATA_FILE_PATH = 'data.csv'

class MyToastNotifier(ToastNotifier):
    def __init__(self):
        super().__init__()

    def on_destroy(self, hwnd, msg, wparam, lparam):
        super().on_destroy(hwnd, msg, wparam, lparam)
        return 0

def send_toast(users_map, updates_map: dict[str,str]):
    body = ""
    if len(updates_map) > 0:
        for key, val in updates_map.items():
            name, _, current_status = users_map[key]
            body = body + name + "\n"

    toast = MyToastNotifier()
    try:
        toast.show_toast(
            "Рейтинговые зменения",
            body,
            duration = 5,
            threaded = True,
        )
    except:
        pass



# clean status string to remove unnecessary characters
def clean_status_string(status_str: str):
    tmp = status_str.replace('\n', '')
    return " ".join(tmp.split())

# prints updates map to terminal
def print_updates(users_map, updates_map: dict[str,str], send_notification: bool = True):
    print('\nСтатус:')
    if len(updates_map) > 0:
        for key, val in updates_map.items():
            name, _, current_status = users_map[key]
            print(f'{name}: изменен с [{current_status}] на [{val}]')
        if send_notification == True:
            send_toast(users_map, updates_map)
    else:
        print('нет изменений')

# applies updates - update data.csv file and clean updates.csv
def apply_updates(users_map, updates_map: dict[str,str]):
    if len(updates_map) > 0:
        for key, val in updates_map.items():
            name, id, _ = users_map[key]
            users_map[key] = (name, id, val)

        with open(DATA_FILE_PATH, mode='w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            if csv_writer:
                for key, val in users_map.items():
                    csv_writer.writerow(val)
                print('Изменения сохранены')

def show_confirm_dialog():
    while True:
        user_input  = input('\nСохранить изменения? (yes/no): ')
        user_choice = user_input.lower()
        if user_choice == 'yes' or user_choice == 'y':
            return True
        elif user_choice == 'no' or user_choice == 'n':
            return False
        else:
            print('Введите yes или no и нажмите Enter')

def do_main():
    print('hello')
    BASE_URL = 'https://ratings.ruchess.ru'
    
    users_map = {}
    updates_map = {}

    with open(DATA_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            id = str(row[1])
            users_map[id] = (str(row[0]), id, str(row[2]))

    for _, val in users_map.items():
        name, id, current_status = val
        print(f'Анализ {name} ФШР ID({id}) ...')
        http_response = requests.get(f'{BASE_URL}/people/{id}')
        if http_response.status_code >= 200 and http_response.status_code < 300:
            soup = BeautifulSoup(http_response.text, features='html.parser')
            item = soup.find('strong', string='Разряд')
            if item:
                status = clean_status_string(item.parent.text)
            else:
                status = 'пусто'
            if str(status) != current_status:
                    print('Смена разряда!')
                    updates_map[id] = status
            else:
                print('Нет изменений')

    print_updates(users_map, updates_map, send_notification=True)

    if len(updates_map) > 0:
        if show_confirm_dialog() == True:
            apply_updates(users_map, updates_map)

if __name__ == '__main__':
    do_main()