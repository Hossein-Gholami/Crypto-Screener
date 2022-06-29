from django.urls import path
from . import views


app_name = "screener"

urlpatterns = [
    # path('stat/', views.getStat, name='stat'),
    path('add/', views.add, name='add_symbol'),
    # path('del/<str:id>/', views.delSymbol, name='del_symbol'),
    # path('/', views.index, name='index'),
    
    # path('run/', views.run),
    # path('<str:room_name>/', views.room, name='room'),
]

"""
steps:
################# ASGI ###################
. urls:
in app urls >>> path('<str:room_name>/', views.room, name='room')

. views:
def room(request, room_name): return render(request, 'screener/room.html', {'room':room_name})

. asgi settings:
1- ASGI_APPLICATION = 'backend.routing.application'
2- CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.pubsub.RedisPubSubChannelLayer',
        or simple 'channels_redis.core.RedisChannelLayer'
        also tried channels.layers.InMemoryChannelLayer but didn't work with celery
        
        'CONFIG': {
            'hosts': [('localhost', 6379)]
        }
    }
}

. create these three files: routing in backend and routing in app and consumers in app

1- backend/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, UrlRouter
from django.core.asgi import get_asgi_application
import app.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        UrlRouter(
            app.routing.websocket_urlpatterns
        )
    )
})

2- screener/routing.py
from django.urls import re_path
from . import consumers

websocket_patterns = [
    re_path(r'ws://app/(?P<room_name>\w+)/', consumers.MyConsumer.as_asgi()),
]

3- screener/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self,text_data):
        json_data = json.loads(text_data)
        # parse data now
        message = json_data['message']
        name = json_data['name']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'name': name
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        name = event['name']

        await self.send(text_data=json.dumps({
            'message': message,
            'name': name
        }))

. now what to do with the template
. inside room.html
if jinja:
    right before <script> tag we have: {{ room_name|json_script:"room-name" }}
    inside the script tag:
        var roomName = JSON.parse(document.get_element_byId("room-name").textContent)

        var chatSocket = new WebSocket(
            'ws://' +
            window.location.host +
            '/ws/screener/' +
            roomName +
            '/'
        )

        function or better to say event handlers
        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data)
        }

        chatSocket.onclose = function(e) {
            console.error('some error message')
        }

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function (e) {
            if (e.keyCode === 13) { // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function (e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message,
                'name': 'Test'
            }));
            messageInputDom.value = '';
        };

if react:
    import { w3cwebsocket as W3CWebSocket } from 'websocket'

    state = {
        isLoggedIn: False,
        messages: [],
        value: '',
        name: '',
        room: 'vacad',
    }

    client = new W3CWebSocket('ws://127.0.0.1:8000/ws/screener/room_name/')

    onButtonClicked = (e) => {
        this.client.send(JSON.stringify({
            type: "message",
            message: this.state.value,
            name: this.state.name
        }))
    }

    componentDidMount() {
        this.client.onopen = () => {
            console.log('websocket client connected')
        }

        this.client.onmessage = (message) => {
            const data = JSON.parse(message.data)
            if (data) {
                this.setState((state) => ({
                    messages: [...state.messages,{
                        msg: data.message,
                        name: data.name
                    }]
                }))
            }
        }

    }

. from here whenever wanted to send to the channel
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

...
async_to_sync(get_channel_layer().group_send)(
    'group_name',
    {
        'type': 'chat_message',
        'message': mymessage,
        'name': 'some name'
    }
)



################# CELERY ###################
1 backend/celery.py
2 backend/__init__.py
3 app/tasks.py
4 backend/settings.py

1. celery.py
import os
from celery import Celery

os.environ.set_default('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = celery('backend')

app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks()

2. __init__.py
from .celery import app as celery_app
__all__ = ('celery_app',)

3. tasks.py
from celery import shared_task

@shared_task()
def add(x,y):
    return x+y

4. settings.py
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'amqp://guest:guest@localhost:5672/')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BROKER', 'redis://localhost:6379/0')

if celery beat desired
CELERY_BEAT_SCHEDULE = {
    'scheduled_task': {
        'task': 'screener.tasks.add',
        'schedule': 5.0,
        'args': (10,10),
    }
}

cons:
after changing channel_layers re-run the server

commands:
1. python manage.py runserver
2. celery -A backend worker -l INFO -P eventlet
3. celery -A backend beat -l INFO
4. celery -A backend flower --port=5555

settings.INSTALLED_APPS+= [
    'channels',
    'django_celery_beat',
    'django_celery_results',
]

"""









