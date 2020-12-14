from django.urls import path,include
from . import views

app_name = 'client'

urlpatterns = [
    path('',views.csv,name='csv'),
]