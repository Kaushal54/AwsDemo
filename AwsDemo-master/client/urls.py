from django.urls import path,include
from . import views

app_name = 'client'

urlpatterns = [
    path('signup/',views.sign_up,name='signup'),
    path('hello/',views.hello,name='hello'),
    path('',views.csv,name='csv'),
]