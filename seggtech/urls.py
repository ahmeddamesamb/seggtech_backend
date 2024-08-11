from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('api/mesures/', mesure_list, name='mesure-list'),
    path('api/mesures/<int:id>/', mesure_detail, name='mesure-detail'),
    path('api/users/', user_list, name='user-list'),
    path('api/users/<int:id>/', user_detail, name='user-detail'),
]

# Ajout des suffixes de format aux URLs (par exemple, .json, .api)
urlpatterns = format_suffix_patterns(urlpatterns)
