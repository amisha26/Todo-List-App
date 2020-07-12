from django.shortcuts import render,redirect
from django.http import HttpResponse
from todo.models import TaskList
from todo.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method=="POST":
        form=TaskForm(request.POST or none)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request,"New Task Added!")
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(manage=request.user) #Task for logged-in user only
        paginator = Paginator(all_tasks, 9)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        return render(request,'todolist.html',{'all_tasks':all_tasks})

def delete_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    if task.manage==request.user:
        task.delete()
    else:
        message.error("Access Restricted, You are not allowed")

    return redirect('todolist')

def edit_task(request,task_id):
    if request.method=="POST":
        task=TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or none, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request,"Task Edited!")
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj':task_obj})

def complete_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    if task.manage==request.user:
        task.done=True
        task.save()
    else:
        message.error("Access Restricted, You are not allowed")
    return redirect('todolist')

def pending_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    task.done=False
    task.save()
    return redirect('todolist')

def index(request):
    context={
        'index_text':"Welcome to index page"
    }
    return render(request,'index.html',context)


def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')