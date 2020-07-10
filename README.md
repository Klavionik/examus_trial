## Examus Restaurant - Тестовое задание для Examus

### Описание

Меню ресторана с расчетом стоимости заказа и добавлением новых блюд по API.

### Запуск
```
$ git clone https://github.com/Klavionik/examus_trrial.git
$ cd examus_trial
$ docker-compose up -d
$ docker-compose exec app python manage.py migrate
$ docker-compose exec app python loaddata fixtures.json
```

### Использование
Приложение: `http://0.0.0.0:8000/`  
[Документация API](https://documenter.getpostman.com/view/9813544/T17M6REW)  
Запуск тестов: `$ docker-compose exec app python manage.py test`  

