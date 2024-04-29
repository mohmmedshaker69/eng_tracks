from django.urls import path, include
from . import views
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import register_user, user_login, user_logout

app_name='api'

router = DefaultRouter()
router.register('course', views.CourseViewSet)
router.register('chapter', views.ChapterViewSet)
router.register('lesson', views.LessonViewSet)
router.register('user', views.UserViewSet)




urlpatterns = [
    path('index/', views.IndexAPIView.as_view()),
    path('detail/<int:pk>/', views.DetailAPIView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('api-auth-token/', obtain_auth_token),
    path('', include(router.urls)),
    path('detail_course/<int:pk>/', views.CourseGetPostAPIView.as_view()),
    path('detail_chapter/<int:pk>/', views.ChapterDetailAPIView.as_view()),
    path('course/<int:pk>/chapters/<int:chapter_pk>/', views.ChapterDetailAPIView.as_view()),
    path('detail_lesson/<int:pk>/', views.LessonDetailAPIView.as_view()),
    path('user/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

  

]