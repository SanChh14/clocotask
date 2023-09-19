from django.urls import path, include
from . import views
from . import usersViews
from . import artistsViews

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('artists/', views.artists, name='artists'),
    path('users/all/',usersViews.show_all_users, name='allusers'),
    path('users/<int:pk>/', usersViews.user_detail),
    path('users/createnewuser/', usersViews.create_user, name='users_createuser'),
    path('users/modifyuser/', usersViews.modify_user, name='modifyuser'),
    path('users/modifyuser/<int:pk>/', usersViews.update_user),
]
