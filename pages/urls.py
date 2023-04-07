from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.page_list, name='page_list'),
    path('<int:pk>/', views.page_detail, name='page_detail'),
    path('new/', views.page_new, name='page_new'),
    path('<int:pk>/edit/', views.page_edit, name='page_edit'),
    path('<int:pk>/delete/', views.page_delete, name='page_delete'),
    path('pages/<int:pk>/', views.page_detail, name='page_detail_by_id'),
]
