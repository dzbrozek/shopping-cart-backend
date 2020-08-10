from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('me/', views.MeAPIView.as_view(), name='me'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
]
