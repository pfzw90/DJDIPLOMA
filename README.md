Для запуска проекта необходимо:

Установить зависимости:

```bash
pip install -r requirements.txt
```

Cоздать базу в postgres и прогнать миграции:

```base
manage.py migrate
```

Выполнить загрузку тестовых данных в базу данных:

```bash
manage.py loaddata fixtures.json
```

Для запуска сервера выполнить команду:

```bash
python manage.py runserver
```
