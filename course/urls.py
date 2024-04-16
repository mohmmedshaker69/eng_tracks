from django.urls import path
from . import views
from django.http import HttpResponseNotFound

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),  
    path('delete/<int:pk>/', views.delete_course, name='delete'),  
    path('delete_chapter/<int:pk>/', views.delete_chapter, name='delete_chapter'),  
    path('delete_lesson/<int:pk>/', views.delete_lesson, name='delete_lesson'),  
    path('chapters/<int:pk>/lessons/', views.LessonView.as_view(), name='lesson'),
    path('addcourse/', views.course_form_view, name='add_course'),
    path('addchapter/<int:pk>/', views.chapter_form_view, name='add_chapters'),
    path('addlesson/<int:pk>/', views.lesson_form_view, name='add_lessons'),
    path('course_detail/<int:pk>/', views.DetailView.as_view(), name='course_detail'),

    path('search/', views.search, name='search'),
    path('edit/<int:pk>/',views.edit, name='edit'),
    path('edit_chapter/<int:pk>/',views.edit_chapter, name='edit_chapter'),



    path('favicon.ico', lambda request: HttpResponseNotFound()),

    
    


    
]
