
from win10toast import ToastNotifier
import csv
import requests
from bs4 import BeautifulSoup
import argparse
import sys
import configparser

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
def print_updates(users_map, updates_map: dict[str,str]):
    print('\nСтатус:')
    if len(updates_map) > 0:
        for key, val in updates_map.items():
            name, _, current_status = users_map[key]
            print(f'{name}, рейтинг изменен:')
            print(f'    старый: {current_status}')
            print(f'    новый : {val}')
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
                csv_writer.writerow(('Имя','ФШР ID','Разряд'))
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
    _, *params = sys.argv
    args = appArgParser.parse_args()

    TARGET_URL = 'https://ratings.ruchess.ru/people'

    config = configparser.ConfigParser()
    with open('config.ini', mode='r', encoding='utf-8') as cfgFile:
        config.read_file(cfgFile)
        TARGET_URL = config['DEFAULT']['target_url']

    users_map = {}
    updates_map = {}

    with open(DATA_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        skip_desc_flag = False
        for row in csv_reader:
            if skip_desc_flag:
                id = str(row[1])
                users_map[id] = (str(row[0]), id, str(row[2]))
            else:
                skip_desc_flag = True

    for _, val in users_map.items():
        name, id, current_status = val
        print(f'Анализ {name} ФШР ID({id}) ...')
        http_response = requests.get(f'{TARGET_URL}/{id}')
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
    
    
    print_updates(users_map, updates_map)

    isDaemon=args.daemon

    if isDaemon == True:
        send_toast(users_map, updates_map)
    else:
        if len(updates_map) > 0:
            if show_confirm_dialog() == True:
                apply_updates(users_map, updates_map)

appArgParser = argparse.ArgumentParser(description='Chess rate tracker',
                                 prog=sys.argv[0],
                                 usage='%(prog)s [OPTIONS]',
                                 epilog='\n')

appArgParser.add_argument('-d', '--daemon',
                    action="store_true",
                    default=False,
                    help='used to specify to launch as daemon')

if __name__ == '__main__':
    do_main()