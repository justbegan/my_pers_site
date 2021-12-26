from django.contrib import admin
from django.urls import path,include
from main_app import views



urlpatterns = [
    path('', views.import_csv),
    path('progress_bar/', views.Get_progress_bar_value.as_view()),
    path('login/', views.loginPage),
    path('logout/', views.logOutUser),
]