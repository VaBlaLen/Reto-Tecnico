from django.urls import path
from . import views



urlpatterns = [
    path('consumtion/', views.ConsumoList.as_view()),
    path('generation/', views.GeneracionList.as_view()),
]