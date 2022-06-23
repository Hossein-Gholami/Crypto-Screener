# Crypto-Screener
Fetches crypto prices with a specified interval

The main functionality in place
![Alt screener](asset/screen1.gif?raw=true "Screener")


This project is an illustration on:
- django and react integration
- celery with django
- django channels

### Usage
user subscribes to some pairs so their prices shall be fetched
these prices will be fetched every 10 seconds

### Technologies
- Django (django-rest-framework, django-channels)
- PostgreSql
- Celery and Celery beat
- RabbitMQ
- React (react-router, react-redux)
