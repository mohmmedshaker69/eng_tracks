from django.urls import path
from . import views
from django.http import HttpResponseNotFound

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),  
    path('delete/<int:pk>/', views.delete_course, name='delete'),  
    path('chapters/<int:pk>/lessons/', views.LessonView.as_view(), name='lesson'),
    path('addcourse/', views.CourseFormView.as_view(), name='add_course'),
    path('addchapter/<int:pk>/', views.ChapterFormView.as_view(), name='add_chapters'),


    path('favicon.ico', lambda request: HttpResponseNotFound()),

    
    





    
]
