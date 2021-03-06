from django.contrib import admin
from django.urls import path, include
from user import views

urlpatterns = [
    # user
    path('login/', views.UserAPIView.as_view()),
    path('logout/', views.UserAPIView.as_view()),
    path('', views.UserView.as_view()),
    path('<obj_id>/', views.UserView.as_view()),
]
