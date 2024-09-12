Django Todo App
## Описание
Django Todo App - это веб приложение по управлению задачами.
Пользователи могут создавать задачи, просматривать, изменять, удалять,
завершать, сортировать, искать по ключевым словам и добавлять в избранное
## API методы
В данной работе используется APIViewsets. Viewsets реализует полный функционал, 
включая просмотр, добавление, изменение и удаление записей.
## Установка
1. Клонируйте репазиторий на свой компьютер:
   git clone https://github.com/Twanivi/diplomsite.git

2. Перейдите в директорию проекта:
   cd sitediplom

3. Установите виртуальное окружение
   python 3 -m venv (имя окружения)    н-р, python 3 venv myproject

4. Активируйте виртуальное окружение:
   - На Windows
     myproject\Scripts\activate

   - На macOS/Linux:
     source myproject/bin/activate

5. Установите зависимости:
   pip install -r requirements.txt

6. Настройте базу данных в файле settings.py
   6.1. Установите базу данных:
        pip install mysqlclient
   
   6.2. При необходимости установите модуль для поодключения к базе данных:
        pip install mysql-connector-python

7. Примените миграции:
   python manage.py migrate

8. Создайте суперпользователя:
   python manage.py createsuperuser

## Запуск
1. Запустите локальный сервер:
   python manage.py runserver

2. Откройте браузер и перейдите по адресу http://127.0.0.1:8000/
