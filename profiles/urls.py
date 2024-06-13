from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('<int:user_id>/onions/', views.ProfileOnionsListView.as_view(), name='profile_onions'),
    path('<int:user_id>/permission/', views.AdjustPermissionView.as_view(), name='adjust_permission'),
]