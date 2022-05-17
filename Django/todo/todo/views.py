from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.
def index(request):
    Todo = ToDo.objects.all()
    Form = TodoForm()
    context = {'Todo':Todo, "TodoForm": Form}
    if request.method == 'POST':
        Form = TodoForm(request.POST)
        if Form.is_valid():
            Form.save()
            return redirect('/')
        else:
            Form = TodoForm()
    return render(request, 'todo/index.html', context)

def delete(request, pk):
    task = ToDo.objects.get(pk=pk)
    context = {'Task': task}
    if request.method == 'POST':
        if 'delete' in request.POST:
            task.delete()
        return redirect('/')
    return render(request, 'todo/delete.html', context)

def edit(request, pk):
    task = ToDo.objects.get(pk=pk)
    Form = TodoForm(instance=task)
    context = {'Task': task, 'TodoForm': Form}
    if request.method == 'POST':
        if 'edit' in request.POST:
            Form = TodoForm(request.POST, instance=task)
            Form.save()
        return redirect('/')
    return render(request, 'todo/edit.html', context)