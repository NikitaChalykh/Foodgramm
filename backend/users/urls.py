from django.urls import path
from djoser.views import TokenCreateView, TokenDestroyView

app_name = 'users'

urlpatterns = [
    path('token/login/', TokenCreateView.as_view(), name='token_login'),
    path('token/logout/', TokenDestroyView.as_view(), name='token_logout')
]
