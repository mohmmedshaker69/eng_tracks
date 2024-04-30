from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from course.models import Course, Chapter, Category, Lesson
from .serializers import UserSerializer, CourseSerializer, CategorySerializer, ChapterSerializer, LessonSerializer, UserSerializer, CourseRatingSerializer, CoursePaymentSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.generics import ListAPIView

from rest_framework import generics, mixins, viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import  AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser, CourseRating, Payment
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter





class SearchCourse(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'category__name', 'category__description']


    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    



    @action(detail=True, methods=['post'], url_name="add_rating",url_path="add_rating")
    def add_rating(self, request, pk):
        course = self.get_object()
        user = User.objects.first()
        request.data.update({'course':course.pk, 'user':user.pk})
        serializer = CourseRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=True, methods=['post'], url_name="pay", url_path="pay")
    def payment(self, request, pk):
        course = self.get_object()
        user = User.objects.first() 

        payment_data = {'course': course.pk, 'user': user.pk}
        serializer = CoursePaymentSerializer(data=payment_data)

        if serializer.is_valid():
            serializer.save()
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





##############################################################################################










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
    