from __future__ import unicode_literals
import secrets
import string
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render, get_object_or_404
from .forms import Join, AddTask
from .models import Project, ScurmBoard
from .filter import Taskfilter


def index(request):
    data = None
    if request.user.is_authenticated:
        me = request.user.username
        you = f"Welcome {me}"
        messages.info(request, you)

        project = Project.objects.filter(
            user_profile__exact=request.user
        )
        data = {'object_list': project}

    return render(request, "Scrum/index.html", data if data else None)


"""
    Renders a form prompting user for classname and related credentials.
"""


def create(request):
    return render(request, "Scrum/upload.html")



def processing(request):
    global new
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(6))
    if request.method == "POST":
        new = Project()
        new.Projectname = request.POST.get('Project_name')
        new.creator = request.user
        new.code = password
        new.save()
    return render(request, "Scrum/create.html", {'password': password, 'creator': new.creator, 'name': new.Projectname})



def join(request):
    global Project
    context = None
    if request.method == 'POST':
        form = Join(request.POST)
        if form.is_valid():
            passcode= form.cleaned_data['join']
            project = Project.objects.all()
            print(project)
            try:
                Project_obj = Project.objects.get(code=passcode)
            except project.DoesNotExist:
                messages.warning(
                    request, 'Sorry, Your password doesn\'t match'
                )
                return render(request, "Scrum/no.html")

            Project_obj.user_profile.add(request.user)
            messages.success(
                request, 'Welcome! Your password was matched successfully!'
            )
            return render(
                request, "Scrum/okay.html",
                {'classrooms': project, 'pswd': passcode}
            )

    else:
        form = Join()
        context = {"form": form}

    messages.info(request, 'Enter the unique passcode below')
    return render(request, "Scrum/join.html", context if context else None)



class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


def Login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'registration/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')


def ScurmProject(request, pk):
    projects = get_object_or_404(Project, pk=pk)
    tasks = projects.scurmboard_set.all()
    Task_filter = Taskfilter(request.GET, queryset=tasks)
    tasks = Task_filter.qs
    return render(request, 'Scrum/ProjectBoard.html', { 'Taskfilter': Task_filter, 'task': tasks, 'project': projects})


def createTask(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'GET':
        return render(request, 'Scrum/addtask.html', {'form':AddTask()})
    else:
        try:
            form = AddTask(request.POST)
            newTask = form.save(commit=False)
            newTask.user = request.user
            newTask.Project = project
            newTask.save()
            return redirect('home')
        except ValueError:
            return render(request, 'Scrum/addtask.html', {'form':AddTask(), 'error':'Bad data passed in. Try again.'})


class Detail_Task(generic.DetailView):
    model = ScurmBoard
    template_name = 'Scrum/Task_Detail.html'