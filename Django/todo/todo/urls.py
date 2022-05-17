from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('delete/<str:pk>', views.delete, name='delete'),
    path('edit/<str:pk>', views.edit, name='edit')

]
