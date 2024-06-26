from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import  ListView,   DetailView, TemplateView, FormView
from .models import Category, Course, Chapter, Lesson, Profile
from django.urls import reverse_lazy, reverse
from .forms import CourseForm, ChapterForm, LessonForm, EditCourseForm, EditChapterForm, SignupForm, ProfileForm, LoginForm, EditAcountForm, ChangePasswordForm
from django.db.models import Q
from django.contrib.auth import authenticate , login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,  update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.models import User



# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['courses'] = Course.objects.all()
        context['categories'] = Category.objects.all()
       
        return context
    

 

def course_form_view(request):

    if request.method=='POST':
        print(request.POST)
        print(type(request.POST))
        form=CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course=form.save(commit=False)
            course.created_by= request.user
            course.save()
            if request.POST.get('submit_action')=='submit':
                return redirect ('index')
            else:
                 return redirect('add_chapters', pk=course.pk)
        
    else:

                form=CourseForm()
                return render(request, 'course_form.html', {
                    'form':form, 
                    'title':'New course'
    })
    
def chapter_form_view(request, pk):
    course = Course.objects.get(pk=pk) 

    if request.method == 'POST':
        form = ChapterForm(request.POST, request.FILES)
        
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.created_by = request.user
            chapter.course = course
            chapter.save()
            
            submit_action = request.POST.get('submit_action')
            if submit_action == 'submit':
                return redirect('index')
            elif submit_action == 'submit and add chapters':
                return redirect('add_chapters', pk=course.pk)
            else:
                return redirect('add_lessons', pk=chapter.pk)
        
    else:
        form = ChapterForm()
    
    return render(request, 'chapter_form.html', {
        'form': form,
        'course': course, 
        'title': 'New chapter'
    })




def lesson_form_view(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.created_by = request.user
            lesson.chapter = chapter
            lesson.save()
            return redirect('index')
    else:
        form = LessonForm()
    
    return render(request, 'lesson_form.html', {
        'form': form,
        'chapter': chapter, 
        'title': 'New lesson'
    })



def edit(request, pk):
    course = get_object_or_404(Course, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditCourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            submit_action = request.POST.get('submit_action')
            if submit_action == 'submit':
                return redirect('index')
            elif submit_action == 'submit and add chapters':
                return redirect('add_chapters', pk=course.pk)
            else:
                return redirect('course_detail', pk=course.pk)
    else:
        form = EditCourseForm(instance=course)
    
    return render(request, 'course_form.html', {
        'form': form, 
        'title': 'Edit course'
    })

def edit_chapter(request,pk):
    chapter=get_object_or_404(Chapter, pk=pk)
    course = chapter.course

    if request.method=='POST':
        form=EditChapterForm(request.POST, request.FILES, instance=chapter)
        if form.is_valid():

            form.save()
            submit_action = request.POST.get('submit_action')
            if submit_action == 'submit':
                return redirect('index')
            elif submit_action == 'submit and add chapters':
                return redirect('add_chapters', pk=course.pk)
            else:
                return redirect('add_lessons', pk=chapter.pk)
        
    else:

                form=EditChapterForm(instance=chapter)
                return render(request, 'chapter_form.html', {
                    'form':form, 
                    'title':'Edit chapter'
    })


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

def delete_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    course_pk = chapter.course.pk
    chapter.delete()
    return redirect('detail', pk=course_pk)


def delete_lesson(request,pk):
    lesson=get_object_or_404(Lesson, pk=pk)
    chapter_pk = lesson.chapter.pk

    lesson.delete()
    return redirect('detail', pk=chapter_pk)
    

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


def dashboard(request):
    courses=Course.objects.filter(created_by=request.user)

    return render(request, 'dashboard.html',{
        'courses':courses,
    })



@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user 
            profile.save()
            return redirect(reverse_lazy('index'))
    else:
        form = ProfileForm()
    return render(request, 'registration/complete.html', {'form': form})



@login_required
def edit_profile(request):
    profile = request.user.profile  
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('index') 
    else:
        form = ProfileForm(instance=profile) 
    return render(request, 'registration/edit_profile.html', {'form': form})


@login_required
def edit_account(request):
    user = request.user
    if request.method == 'POST':
        form = EditAcountForm(request.POST,  instance=user)
        if form.is_valid():
        
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = EditAcountForm(instance=user)
    return render(request, 'registration/edit_account.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if request.user.is_authenticated and email == request.user.email:
                form.add_error('email', "You are already registered with this email.")
            elif User.objects.filter(email=email).exists():
                form.add_error('email', "This email address is already in use. Please use a different email.")
            else:
                user = form.save()
                login(request, user)  
                return redirect('profile')  
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')


    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user) 
            return super().form_valid(form)

        return super().form_invalid(form)
    

    
class CustomLogoutView(LogoutView):
    next_page =reverse_lazy('index')





def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('index')  
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})



# class SignupView(FormView):
#     template_name = 'registration/signup.html'
#     form_class = SignupForm
#     success_url = reverse_lazy('index')

#     def form_valid(self, form):
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password1']
#         form.save()
#         user = authenticate(username=username, password=password)
#         login(self.request, user)
#         return super().form_valid(form)


# def signup(request):

#     if request.method == 'POST':
#         form = SignupForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('index')
        
#     else:    

#         form=SignupForm()

#     return render(request, 'registration/signup.html', {
#         'form': form
#     })

# def profile(request):
#     profile = Profile.objects.get(user=request.user)
#     return render(request,'registration/profile.html',{'profile':profile})

# def profile(request):
#     if request.method == 'POST': 
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
           
#             return redirect(reverse_lazy('index'))

#     else: 
#         form = ProfileForm()

#     return render(request,'registration/complete.html',{'form':form})





# class ChapterFormView(TemplateView):
#     template_name = 'chapter_form.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         course = self.get_course()
#         context['chapter_form'] = ChapterForm(course=course)
#         course_pk = self.request.GET.get('course_pk') 
#         if course_pk:
#             course = Course.objects.get(pk=course_pk)  
#             context['course'] = course
#         return context
    
#     def get_course(self):
#         course_id = self.kwargs.get('course_id')
#         course = get_object_or_404(Course, pk=course_id)
#         return course

#     def post(self, request, *args, **kwargs):
#         course = self.get_course()
#         chapter_form = ChapterForm(request.POST, request.FILES, course=course)  
#         if chapter_form.is_valid():
#             chapter_form.save()
#             return redirect('course_detail', course_id=course.pk)
#         else:
         
#             context = self.get_context_data()
#             context['chapter_form'] = chapter_form
#             return self.render_to_response(context)

   


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


# class ChangePasswordView(PasswordChangeView):
#     form_class = ChangePasswordForm
#     template_name = 'registration/password_change.html'
#     success_url = reverse_lazy('index') 

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         update_session_auth_hash(self.request, form.user)
#         return response
