from django.db import models
from course.models import Course
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=14)
    address = models.TextField()
    student = models.BooleanField(default=False, null=True, blank=True)
    learning_place = models.CharField(max_length=150, null=True, blank=True)
    employee = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    # Define related_name attribute to avoid clashes with auth.User model
    related_name = 'custom_user_groups'

    def __str__(self):
        return self.username
    

class CourseRating(models.Model):
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='course_ratings', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  

    class Meta:
        unique_together = ('course', 'user')  

    def __str__(self):
        return f"{self.stars} stars for {self.course} by {self.user}"
    

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Payment(models.Model):
    course = models.ManyToManyField(Course, related_name='payment')
    payment_method = models.ForeignKey(PaymentMethod, related_name='payment_method',on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name='buys', on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='active')

    def is_amount_paid_equal_to_price(self):
    
        if self.amount_paid is not None and self.course.price is not None:
            return self.amount_paid == self.course.price
        return False

    @property
    def expired_at(self):

        if self.purchased_at and self.course.duration:
            return self.purchased_at + self.course.duration


    def deactivate_if_expired(self):

        if timezone.now() > self.expired_at:
            self.status = 'inactive'
            self.save(update_fields=['status'])
            return self.status
        

    def __str__(self):
        return f"{self.user} bought {self.course} at {self.purchased_at}"


