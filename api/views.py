from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from course.models import Course, Chapter, Category, CourseRating, Lesson, Profile
from rest_framework.decorators import api_view
from .serializers import UserSerializer, CourseSerializer, CategorySerializer, ChapterSerializer, LessonSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import  AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import permissions





class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (AllowAny,)


    @action(detail=True, methods=['post'], url_name="add_chapter",url_path="add_chapter")
    def create_chapter(self, request, pk):
        course = self.get_object()
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all().prefetch_related('course')
    serializer_class = ChapterSerializer
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['post'], url_name="add_lesson",url_path="add_lesson")
    def create_lesson(self, request, pk):
        chapter = self.get_object()
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chapter=chapter)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().prefetch_related('chapter')
    serializer_class = LessonSerializer
    permission_classes = (AllowAny,)
















class IndexAPIView(APIView):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        categories = Category.objects.all()

        course_serializer = CourseSerializer(courses, many=True)
        category_serializer = CategorySerializer(categories, many=True)

        return Response({
            'courses': course_serializer.data,
            'categories': category_serializer.data
        })
    


class DetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        
        course = get_object_or_404(Course, pk=pk)
        course_serializer = CourseSerializer(course)

        chapters = Chapter.objects.filter(course=course)
        lessons = Lesson.objects.filter(chapter__in=chapters)

        chapter_serializer = ChapterSerializer(chapters, many=True)
        lesson_serializer = LessonSerializer(lessons, many=True)

   
        data = {
            'course': course_serializer.data,
            'chapters': chapter_serializer.data,
            'lessons': lesson_serializer.data,
        }

        return Response(data)
    


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)




class CourseGetPostAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        
        course = get_object_or_404(Course, pk=pk)
        course_serializer = CourseSerializer(course)
        data = {
            'course': course_serializer.data,
        }

        return Response(data)
    
    def post(self,request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    


class  CourseGetPutDeleteApiView(APIView):

    def get_object(self, pk):

        return get_object_or_404(Course, pk=pk)

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class ChapterDetailAPIView(APIView):
    def get(self, request, pk, chapter_pk=None, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        if chapter_pk is not None:
            chapter = get_object_or_404(Chapter, pk=chapter_pk, course=course)
            chapter_serializer = ChapterSerializer(chapter)
            return Response(chapter_serializer.data)
        else:
            chapters = Chapter.objects.filter(course=course)
            chapter_serializer = ChapterSerializer(chapters, many=True)
            data = {'chapters': chapter_serializer.data}
            return Response(data)
        

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        chapter_serializer = ChapterSerializer(data=request.data)
        if chapter_serializer.is_valid():
            chapter_serializer.save(course=course)
            return Response(chapter_serializer.data, status=status.HTTP_201_CREATED)
        return Response(chapter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class  ChapterGetPutDeleteApiview(APIView):

    def get_object(self, pk):

        return get_object_or_404(Course, pk=pk)

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        
        course = get_object_or_404(Course, pk=pk)
        chapters = get_object_or_404(Chapter, course=course)
        lessons = Lesson.objects.filter(chapter__in=chapters)

        lesson_serializer = LessonSerializer(lessons, )

   
        data = {
            'lessons': lesson_serializer.data,
        }

        return Response(data)
    
    def post(self,request, pk):
        course = get_object_or_404(Course, pk=pk)
        chapters = get_object_or_404(Chapter, course=course)

        lesson_serializer = LessonSerializer(data=request.data,)
        if lesson_serializer.is_valid():
            lesson_serializer.save(chapter__in=chapters)
            return Response(lesson_serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    