# Foodram

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)<br/>
![yamdb workflow](https://github.com/zerg959/foodgram-project-react/workflows/foodgram_workflow/badge.svg)
<br/>

Проект развернут по адресу http://84.201.139.255<br>

админ 123@123.ru<br>
пароль 123qweQWE<br>

Установите Docker и Docker-compose. Запустите сборку образов:<br>
sudo docker-compose up<br>
или
sudo docker-compose up -d --build<br>

После развертывания проекта создайте миграции и заполнените базу данных:<br>
```
sudo docker-compose exec backend python manage.py collectstatic --noinput
```
```
sudo docker-compose exec backend python manage.py migrate --noinput
```

- Для создания суперпользователя введите команду:
```
sudo docker-compose exec backend python manage.py createsuperuser
```

Для запуска на удаленном сервере:<br>
+ отредактируйте файл infra/nginx/default.conf<br>

+ в строке server_name необходимо вписать IP своего сервера<br>

+ Установите на сервер docker и docker-compose<br>

+ Скопируйте файлы docker-compose.yml и default.conf из директории infra и infra/nginx на сервер<br>

Cоздайте на сервере в директории с проектом .env файл c данными авторизации:

```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
SECRET_KEY=<секретный ключ> 
```
Добавьте в Secrets GitHub переменные:<br>
```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
SECRET_KEY=<секретный ключ>

DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для ssh, если он имеется>
SSH_KEY=<SSH ключ>
```
Для получения уведомлений в телеграме о статусе деплоя:<br>
```
TELEGRAM_TO=<ID чата>
TELEGRAM_TOKEN=<токен вашего бота>
```
Для доступа в развернутый контейнер используйте команду:<br>
```
sudo docker -it exec <NAME_CONTAINER or ID_CONTAINER> bash

```