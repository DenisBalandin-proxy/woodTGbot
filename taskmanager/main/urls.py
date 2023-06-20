from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('benefits/<int:chat_id>/<uuid:session_id>/<str:fio>/<str:benefit>/<int:sum>', views.show_application, name='upload_file'),
    path('result' , views.benefit_application, name='success'),
    path('benefitsinfo', views.about_benefits, name='about+benefits'),
    path('', views.home_page)
]