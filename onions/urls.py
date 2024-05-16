from django.urls import path
from . import views

urlpatterns = [
    path('', views.OpinionView.as_view()),
    path('<int:pk>', views.OpinionView.as_view()),
]