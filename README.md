# Foodram

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)<br/>
![yamdb workflow](https://github.com/zerg959/foodgram-project-react/workflows/foodgram_workflow/badge.svg)
<br/>

Проект развернут по адресу http://84.201.139.255

админ zerg959@yandex.ru
пароль 123zzzZZZ

Установите Docker и Docker-compose. Запустите сборку образов:
sudo docker-compose up
или
sudo docker-compose up -d --build
После развертывания проекта создайте миграции и заполнените базу данных:
sudo docker-compose exec python manage.py migrate
sudo docker-compose exec python manage.py createsuperuser
sudo docker-compose exec python manage.py collectstatic
