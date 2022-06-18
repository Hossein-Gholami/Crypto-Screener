from django.urls import path
from . import views


app_name = "screener"

urlpatterns = [
    path('pairs/', views.getPairs, name="pairs"),
]
