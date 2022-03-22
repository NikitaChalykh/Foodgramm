from django.urls import path

from .views import delete_token, get_token

app_name = 'users'

urlpatterns = [
    path('login/', get_token, name='get_token'),
    path('logout/', delete_token, name='delete_token')
]
