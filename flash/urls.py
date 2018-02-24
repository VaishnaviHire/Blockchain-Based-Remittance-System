from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^play', views.play, name="play"),
    url(r'^login', views.login, name="login"),
    url(r'^logout', views.logout_user, name="logout"),
    url(r'^routes', views.routes, name="routes"),
    url(r'^todo', views.CreateLists.as_view(), name="lists"),
    url(r'^getdirections', views.get_directions, name="get_directions"),
    url(r'^search(?P<user_id>[0-9]+)/$', views.StartSearch.as_view(), name="search"),
    url(r'^view_list', views.view_list, name="view_list"),
    url(r'^ajax/add_new_task', views.add_new_task, name="add_new_task"),
    url(r'^delete_task(?P<id>[0-9]+)/$', views.delete_task, name="delete_task"),
    url(r'^registration_form', views.UserFormView.as_view(), name="registration_form"),
    url(r'^(?P<album_id>[0-9]+)/$', views.details, name="details"),
    url(r'^start_search(?P<user_id>[0-9]+)/$', views.start_search, name="start_search"),
    url(r'^wallet', views.wallet, name="wallet"),
    url(r'^transfer', views.TransferFormView.as_view(), name="transfer"),
    url(r'^add_to_wallet', views.AddWalletView.as_view(), name="add_to_wallet"),

]