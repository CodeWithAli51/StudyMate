from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import TemplateView

from academics.models import Subject

from .forms import StudyTaskForm
from .models import StudyTask


class PlannerIndexView(TemplateView):
    template_name = 'planner/index.html'


def _stamp_completion(task):
    if task.status == StudyTask.STATUS_COMPLETED and task.completed_at is None:
        task.completed_at = timezone.now()
    elif task.status != StudyTask.STATUS_COMPLETED:
        task.completed_at = None


@login_required
def task_list(request):
    tasks = StudyTask.objects.filter(student=request.user).select_related(
        'subject', 'chapter', 'topic'
    )
    subject_id = request.GET.get('subject')
    status = request.GET.get('status')
    if subject_id:
        tasks = tasks.filter(subject__pk=subject_id)
    if status in dict(StudyTask.STATUS_CHOICES):
        tasks = tasks.filter(status=status)
    return render(request, 'planner/task_list.html', {
        'tasks': tasks,
        'subjects': Subject.objects.all(),
        'statuses': StudyTask.STATUS_CHOICES,
        'active_subject': subject_id or '',
        'active_status': status or '',
    })


@login_required
def task_create(request):
    if request.method == 'POST':
        form = StudyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.student = request.user
            _stamp_completion(task)
            task.save()
            messages.success(request, 'Task created.')
            return redirect('planner:task_list')
    else:
        form = StudyTaskForm()
    return render(request, 'planner/task_form.html', {
        'form': form, 'heading': 'New task',
    })


@login_required
def task_update(request, pk):
    task = get_object_or_404(StudyTask, pk=pk, student=request.user)
    if request.method == 'POST':
        form = StudyTaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            _stamp_completion(task)
            task.save()
            messages.success(request, 'Task updated.')
            return redirect('planner:task_list')
    else:
        form = StudyTaskForm(instance=task)
    return render(request, 'planner/task_form.html', {
        'form': form, 'heading': 'Edit task', 'task': task,
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(StudyTask, pk=pk, student=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('planner:task_list')
    return render(request, 'planner/task_confirm_delete.html', {'task': task})


@login_required
def task_complete(request, pk):
    task = get_object_or_404(StudyTask, pk=pk, student=request.user)
    if request.method == 'POST':
        task.status = StudyTask.STATUS_COMPLETED
        _stamp_completion(task)
        task.save()
        messages.success(request, 'Task marked complete.')
    return redirect('planner:task_list')
