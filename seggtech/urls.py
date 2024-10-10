from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

urlpatterns = [
    path('sensor-data', mesure_list, name='mesure-list'),
    path('sensor-data/<int:id>', mesure_detail, name='mesure-detail'),
    path('users', user_list, name='user-list'),
    path('users/<int:id>/archive', archive_user, name='archive_user'),
    path('users/<int:id>/activate', activate_user, name='activate_user'),
    path('users/<int:id>', user_detail, name='user-detail'),
    path('login', login_view, name='login_view'),
    path('logout', logout_view, name='logout_view'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('store-sensor-data', store_sensor_data, name='store_sensor_data'),
    path('get-sensor-data', get_sensor_data, name='get_sensor_data'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
