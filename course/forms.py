from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from .models import Course, Chapter, Lesson

class LoginForm(AuthenticationForm):
     username= forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))    
     password= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))         
    



class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username', 'email', 'password1', 'password2')

    username= forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))    

    email= forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'your email',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))    

    password1= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))    

    password2= forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'repeat pass',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))    

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'objectives': forms.TextInput(attrs={'class': 'form-control'}),
            'requirment': forms.TextInput(attrs={'class': 'form-control'}),
            'resources': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control'}),  
            'price': forms.NumberInput(attrs={'class': 'form-control'}),  
        }


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ('name', 'description', 'content')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description':forms.TextInput(attrs={'class': 'form-control'}),
            'content':forms.TextInput(attrs={'class': 'form-control'}),

        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('name', 'video', 'pdf')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'video':forms.FileInput(attrs={'class': 'form-control'}),
            'pdf':forms.FileInput(attrs={'class': 'form-control'}),

        }

class EditCourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=( 'name', 'description', 'price', 'image', 'active')

        widgets={
       
         'name':forms.TextInput(attrs={
            'class': 'form-control'
        }),
         'description':forms.Textarea(attrs={
            'class': 'form-control'
        }),
         'price':forms.TextInput(attrs={
            'class': 'form-control'
        }),
         'image':forms.FileInput(attrs={
            'class': 'form-control'
        })
    }

class EditChapterForm(forms.ModelForm):
    class Meta:
        model=Chapter
        fields=( 'name', 'description')

        widgets={
       
         'name':forms.TextInput(attrs={
            'class': 'form-control'
        }),
         'description':forms.Textarea(attrs={
            'class': 'form-control'
        }),
        
    }
    