from django.shortcuts import render, redirect, get_object_or_404
# from .forms import SignupForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, TemplateView
from .models import Category, Course, Chapter, CourseRating, Enrollment, Lesson
from django.urls import reverse_lazy
from .forms import CourseForm, ChapterForm

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['courses'] = Course.objects.all()
        context['categories'] = Category.objects.all()
       
        return context
    

    
class CourseFormView(TemplateView):
    template_name = 'course_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courseform'] = CourseForm()
        return context

    def post(self,request,*args,**kwargs):
        courseform = CourseForm(request.POST, request.FILES)
        if courseform.is_valid():
            courseform.save()
     
     
        return redirect('index')
    
   
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from .forms import ChapterForm
from .models import Course

class ChapterFormView(TemplateView):
    template_name = 'chapter_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_course()
        context['chapter_form'] = ChapterForm(course=course)
        return context
    
    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        return course

    def post(self, request, *args, **kwargs):
        chapter_form = ChapterForm(request.POST, request.FILES)  
        if chapter_form.is_valid():
            chapter_form.save()
        return redirect('index')


class DetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        course = self.get_object()

        chapters = Chapter.objects.filter(course=course)
        lessons = Lesson.objects.filter(chapter__in=chapters)#

        context['categories'] = Category.objects.all()
        context['chapters'] = chapters
        context['lessons'] = lessons

        return context

           



class ChapterView(ListView):
    model = Chapter
    queryset = Chapter.objects.all()
    context_object_name = 'chapters'
    template_name = 'chapters.html'



class LessonView(TemplateView):
    template_name = 'lesson.html'
     
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        print(self.kwargs)
        print(type(self.kwargs))
        context = super().get_context_data(**kwargs)

        chapter = get_object_or_404(Chapter, pk=pk)
        lessons = Lesson.objects.filter(chapter=chapter)

        context['chapter'] = chapter
        context['lessons'] = lessons
        print(pk)
        return context
    
        
def delete_course(request,pk):
    course=get_object_or_404(Course, pk=pk, created_by=request.user)
    course.delete()
    return redirect('index')
    





# def signup(request):

#     if request.method == 'POST':
#         form = SignupForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('/login/')
        
#     else:    

#         form=SignupForm()

#     return render(request, 'signup.html', {
#         'form': form
#     })
