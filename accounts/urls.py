from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('createnewuser/', views.createNewUser, name='createuser'),
    path('logout/', views.logout, name='logout'),
]