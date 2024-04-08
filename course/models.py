from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Course(models.Model):
    created_by=models.ForeignKey(User, related_name='course',on_delete=models.PROTECT)   
    category = models.ForeignKey(Category, related_name='course' ,on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.TextField()
    objectives = models.TextField()
    requirment = models.TextField()
    resourses = models.TextField()
    image = models.ImageField(upload_to='photos')
    active = models.BooleanField(default=True)
    hours = models.IntegerField()
    price = models.IntegerField()
    chapters_count = models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.name
    

class CourseRating(models.Model):
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='course_ratings', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  ###

    class Meta:
        unique_together = ('course', 'user')  # Each user can only rate a course once

    def __str__(self):
        return f"{self.stars} stars for {self.course} by {self.user}"


class Chapter(models.Model):
    course = models.ForeignKey(Course, related_name='course', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    @property
    def lessons_count(self):
        return self.lessons.count()

    class Meta:
        ordering=['created_at']
    
    def __str__(self):
        return self.name

class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='lessons', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    video = models.FileField(upload_to='videos/')
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    course = models.ForeignKey(Course, related_name='buys', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='buys', on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user} bought {self.course} at {self.purchased_at}"



