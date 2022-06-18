# Crypto-Screener
Fetches crypto prices with a specified interval

This project is an illustration on how-to:
- django and react integration
- celery with django
- django channel
- dockerize these components

### Use Case
user subscribes to some pairs so their prices shall be fetched
default coins: [Bitcoin, Ether, Solana]
these prices will be fetched every 5 or so minutes

### Technologies
- Django (django-rest-framework, django-channel)
- PostgreSql
- Celery
- RabbitMQ
- React (react-router, react-redux)
