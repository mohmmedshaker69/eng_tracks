from django.shortcuts import render, redirect, get_object_or_404
# from .forms import SignupForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, TemplateView
from .models import Category, Course, Chapter, CourseRating, Enrollment, Lesson
from django.urls import reverse_lazy
from .forms import CourseForm, ChapterForm
from django.db.models import Q


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['courses'] = Course.objects.all()
        context['categories'] = Category.objects.all()
       
        return context
    

    


# class CourseFormView(TemplateView):
#     template_name = 'course_form.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['courseform'] = CourseForm()
#         course_pk = self.request.GET.get('course_pk') 
#         if course_pk:
#             course = Course.objects.get(pk=course_pk) 
#             context['course'] = course
#         return context

#     def post(self, request, *args, **kwargs):
#         courseform = CourseForm(request.POST, request.FILES)
#         if courseform.is_valid():
#             courseform.save()
#             return redirect('index')
#         else:
#             return render(request, self.template_name, {'courseform': courseform})



def course_form_view(request):

    if request.method=='POST':
        form=CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course=form.save(commit=False)
            course.created_by= request.user
            course.save()
            return redirect ('index')
        
    else:

                form=CourseForm()
                return render(request, 'course_form.html', {
                    'form':form, 
                    'title':'New course'
    })


class ChapterFormView(TemplateView):
    template_name = 'chapter_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_course()
        context['chapter_form'] = ChapterForm(course=course)
        course_pk = self.request.GET.get('course_pk') 
        if course_pk:
            course = Course.objects.get(pk=course_pk)  
            context['course'] = course
        return context
    
    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        return course

    def post(self, request, *args, **kwargs):
        course = self.get_course()
        chapter_form = ChapterForm(request.POST, request.FILES, course=course)  
        if chapter_form.is_valid():
            chapter_form.save()
            return redirect('course_detail', course_id=course.pk)
        else:
         
            context = self.get_context_data()
            context['chapter_form'] = chapter_form
            return self.render_to_response(context)



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
    

def search(request):
      category_id=request.GET.get('category',0)#
      query= request.GET.get('query','')
      categories=Category.objects.all()
      courses=Course.objects.filter(active=True)
      
      if category_id:
            courses=courses.filter(category_id=category_id)

      if query:
            courses=courses.filter(Q(name__icontains=query) | Q(description__icontains=query))

      return render(request, 'search.html',{
            'courses':courses,
            'query':query,
            'categories':categories,
            'category_id':int(category_id),

      })




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
