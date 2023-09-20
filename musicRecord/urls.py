from django.urls import path, include
from . import views
from . import usersViews
from . import artistsViews
from . import songsViews
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('artists/', views.artists, name='artists'),
    path('users/all/',usersViews.show_all_users, name='allusers'),
    path('users/<int:pk>/', usersViews.user_detail),
    path('users/createnewuser/', usersViews.create_user, name='users_createuser'),
    path('users/modifyuser/', usersViews.modify_user, name='modifyuser'),
    path('users/modifyuser/<int:pk>/', usersViews.update_user),
    path('artists/all/',artistsViews.show_all_artists, name='allartists'),
    path('artists/<int:pk>/', artistsViews.artist_detail),
    path('artists/addnewartist/', artistsViews.create_artist, name='createartist'),
    path('artists/modifyartist/', artistsViews.modify_artist, name='modifyartist'),
    path('artists/modifyartist/<int:pk>/', artistsViews.update_artist),
    path('artists/<int:pk>/songs/', songsViews.artist_songs),
    path('artists/<int:pk>/songs/<int:spk>/', songsViews.song_detail),
    path('artists/<int:pk>/addnewsong/', songsViews.add_song),
    path('artists/<int:pk>/modifysong/', songsViews.modify_songs),
    path('artists/<int:pk>/modifysong/<int:spk>/', songsViews.update_song),
]
