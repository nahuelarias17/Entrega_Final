from django.urls import path
from . import views

app_name = 'blog_messages'



urlpatterns = [
    path('', views.home, name='home'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('outbox/', views.outbox_view, name='outbox'),
    path('send/', views.send_message_view, name='send_message'),
    path('view/<int:message_id>/', views.view_message, name='view_message'),
    path('messages_section/', views.messages_section, name='messages_section'),
]
