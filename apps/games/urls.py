from django.urls import path
from .views import GameSearchViewSet

urlpatterns = [
    path('games/search/', GameSearchViewSet.as_view({'get': 'list'}), name='game-search'),
   
]
