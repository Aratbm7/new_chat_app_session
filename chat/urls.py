from django.urls import path
from . import views


urlpatterns = [
    path('', views.room , name='room'),
    # path('chat/<str:room_name>/', views.room , name='room'),
]
