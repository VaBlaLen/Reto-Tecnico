from django.urls import path
from . import views



urlpatterns = [
    path('generation/', views.GeneracionList.as_view()),
    path('consumption/', views.ConsumoList.as_view()),
]