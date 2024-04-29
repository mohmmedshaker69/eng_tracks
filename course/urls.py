from django.urls import path
from . import views
from django.http import HttpResponseNotFound
from .views import CustomLogoutView
from django.views.generic import TemplateView


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
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/',views.signup , name='signup'),
    path('profile',views.profile , name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout', views.CustomLogoutView.as_view(), name='logout'),
    path('change_password', views.change_password, name='change_password'),\
    path('about/', TemplateView.as_view(template_name='setting.html'), name='setting'),
    ###########################


    path('favicon.ico', lambda request: HttpResponseNotFound()),

    
]
