from django.urls import path
from . import views

urlpatterns = [
    path('<int:onion_id>', views.OpinionView.as_view()),
    path('onionlist/', views.OpinionListView.as_view()),
    path('onionvisualize/<int:pk>', views.onion_visualize),
]
