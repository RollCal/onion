from django.urls import path
from .views import PiesAPIView
urlpatterns = [
    path('<int:pie_id>/', PiesAPIView.as_view()),
]