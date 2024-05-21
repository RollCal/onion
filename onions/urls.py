from django.urls import path
from . import views

urlpatterns = [
    path('', views.OpinionView.as_view()),
    path('<int:onion_id>', views.OpinionView.as_view()),
    path('onionlist/', views.OpinionListView.as_view()),
]
