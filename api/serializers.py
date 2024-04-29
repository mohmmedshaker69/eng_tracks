from course.models import Course, Chapter,Category ,CourseRating,Lesson, Profile
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}



class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Category
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta :
        model = Course
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):

    course = CourseSerializer()

    class Meta :
        model = Chapter
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    # chapter = ChapterSerializer()

    class Meta :
        model = Lesson
        fields = '__all__'