from django.urls import path
from .views import PiesAPIView
urlpatterns = [
    path('<str:object_name>/<int:object_id>/', PiesAPIView.as_view()),
]