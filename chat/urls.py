from django.urls import path
from . import views


urlpatterns = [
    # path('chat/<str:room_name>/', views.answer_to_chat , name='room'),
    path('', views.room , name='room'),
    path('chats/', views.chat_list, name='chat_list'),
]
    