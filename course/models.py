from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14)
    image = models.ImageField(upload_to='photos', null=True, blank=True)
    address = models.TextField()
    student = models.BooleanField(default=False, null=True, blank=True)
    learning_place = models.CharField(max_length=150, null=True, blank=True)
    employee = models.BooleanField(default=False, null=True, blank=True)


  
    def __str__(self):
        return self.user.username

 




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
    name = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    objectives = models.TextField(null=True, blank=True)
    requirment = models.TextField(null=True, blank=True)
    resourses = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='photos', null=True, blank=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    hours = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    @property
    def chapters_count(self):
        return self.chapters.count()
    
    def __str__(self):
        return self.name
    

class CourseRating(models.Model):
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='course_ratings', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  

    class Meta:
        unique_together = ('course', 'user')  # Each user can only rate a course once

    def __str__(self):
        return f"{self.stars} stars for {self.course} by {self.user}"


class Chapter(models.Model):
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)
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





# @receiver(post_save , sender=User)
# def create_user_profile(sender,instance,created , **kwargs):
#     if created:
#         Profile.objects.create(
#             user = instance
#         )


