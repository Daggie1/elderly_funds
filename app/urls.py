
from django.urls import path
from django.contrib.auth.views import LogoutView
from .view.report import report
import  users.views as users_app_view

urlpatterns = [
    path('', report, name='home'),
    path('login/', users_app_view.Login.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
    # Auth
    path('users/', users_app_view.UserListView.as_view(), name='users.index'),
    path('elderlys/', users_app_view.ElderlyListView.as_view(), name='users.elderly'),
    path('guardians/', users_app_view.GuardiansListView.as_view(), name='users.guardians'),
    path('users/', users_app_view.UserListView.as_view(), name='users.index'),
    path('users/create/', users_app_view.user_create, name='users.create'),
    path('create/elderly', users_app_view.elderly_create, name='users.create.elderly'),
    path('users/create/<int:elderly_id>/guardian', users_app_view.guardian_create, name='users.create.guardian'),

    path('users/<int:pk>/', users_app_view.UserDetailView.as_view(), name='users.detail'),
    path('profile/', users_app_view.profile, name='profile'),
    path('users/update/<int:pk>/', users_app_view.UserUpdateView.as_view(), name='user.update'),
    path('change_password/<username>', users_app_view.change_password, name='user.changepass'),

    path('user/delete/<int:pk>/', users_app_view.UserDeleteView.as_view(), name='user.delete'),

    # groups
    path('roles/', users_app_view.GroupListView.as_view(), name='groups.index'),
    path('roles/create/', users_app_view.add_group, name='roles.create'),
    path('roles/update/<int:pk>/', users_app_view.GroupUpdateView.as_view(), name='groups.update'),
    path('roles/delete/<int:pk>/', users_app_view.GroupDeleteView.as_view(), name='groups.delete'),
    #
]

