from django.urls import include, path
from rest_framework import routers

app_name = 'api'

router_api = routers.DefaultRouter()

# router_v1.register('categories', CategoryViewSet)
# router_v1.register('genres', GenreViewSet)
# router_v1.register('titles', TitleViewSet)
# router_v1.register('users', UserViewSet)

urlpatterns = [
    path('/', include(router_api.urls))
]
