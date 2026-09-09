from django.shortcuts import render, redirect
from django.db.models import Case, When, Value, IntegerField
from .models import Task

def index(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority', 'Medium')
        if title:
            Task.objects.create(title=title, priority=priority)
        return redirect('index')

    tasks = Task.objects.annotate(
        priority_order=Case(
            When(priority='High', then=Value(1)),
            When(priority='Medium', then=Value(2)),
            When(priority='Low', then=Value(3)),
            output_field=IntegerField(),
        )
    ).order_by('priority_order')

    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    percent = int((completed / total) * 100) if total else 0

    return render(request, 'todo/index.html', {
        'tasks': tasks, 'total': total, 'completed': completed, 'percent': percent
    })

def toggle_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

def delete_task(request, task_id):
    Task.objects.filter(id=task_id).delete()
    return redirect('index')