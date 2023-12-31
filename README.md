# Сhess Rating Tracker

## Установка

1. Устанавливаем python 3.10 с сайта https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
2. Устанавливаем библиотеки из консоли:
```console
pip install win10toast
pip install requests
pip install beautifulsoup4
```

## Настройка базы данных учеников
Открываем data.csv файл в текстовом редакторе (Excel не понимает енкодинга).
Добавляем учеников в формате Имя,ФШР_ID,Рейтинг (**запятые обязательно - они являются разделителями**).
***Пример***: добавление нового ученика Иванов Иван c ФШР_ID 674737:

    data.csv
    Петров Александр,43234,Разряд МС
    Сидоров Сергей,555632,Разряд 1Ю
    Иванов Иван,674737, <--- Рейтинг можно не ставить для нового ученика

## Запуск программы
 - **chess_tracker.bat** - запускает программу в интерактивном режиме (программа будет ждать подтверждения от пользователя если есть изменения)
 - **chess_tracker_svc.bat** - запускает программу в фоновом режиме (программа просто пошлет нотификацию если есть изменения)

## Как работает программа
При запуске программа считывает бызу данных учеников. По каждому собирает статистику рейтинга с сайта ratings.ruchess.ru.
Если рейтинг с сайта не соответствует рейтингу в базе - то программа сообщает об этом и ждет подтверждения для обновления рейтинга в базе.

## Пример
*Пуск первый*

    # Состояние базы данных data.csv:
    Имя,ФШР ID,Разряд
    Кандрашина Мирослава,415400,
    Шимгаев Дмитрий,361302,
   
    # Запуск
    D:\git\chess_tracker>chess_tracker.bat
    Анализ Кандрашина Мирослава ФШР ID(415400) ...
    Смена разряда!
    Анализ Шимгаев Дмитрий ФШР ID(361302) ...
    Смена разряда!
    
    Статус:
    Кандрашина Мирослава, рейтинг изменен:
        старый:
        новый : Разряд: 1 юношеский разряд (действует до 31.08.2025)
    Шимгаев Дмитрий, рейтинг изменен:
        старый:
        новый : пусто
    
    Сохранить изменения? (yes/no): y
    Изменения сохранены
        
    # Состояние базы данных data.csv:
    Имя,ФШР ID,Разряд
    Кандрашина Мирослава,415400,Разряд: 1 юношеский разряд (действует до 31.08.2025)
    Шимгаев Дмитрий,361302,пусто

*Пуск второй*

    # Запуск
    D:\git\chess_tracker>chess_tracker.bat
    Анализ Кандрашина Мирослава ФШР ID(415400) ...
    Нет изменений
    Анализ Шимгаев Дмитрий ФШР ID(361302) ...
    Нет изменений
    
    Статус:
    нет изменений
