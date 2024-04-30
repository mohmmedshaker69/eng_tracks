from django.contrib import admin
from course.models import Category, Chapter, Course, Lesson, Profile
from api.models import CourseRating
admin.site.register(Profile)
admin.site.register(CourseRating)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description') 

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_by', 'price', 'active')  
    list_filter = ('category', 'active')  
    search_fields = ('name', 'description') 


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'created_at')  
    list_filter = ('course',)  

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter') 
    list_filter = ('chapter__course',)  




