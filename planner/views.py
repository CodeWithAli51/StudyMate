from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import TemplateView

from academics.models import Subject

from .forms import StudySessionFinishForm, StudyTaskForm
from .models import StudySession, StudyTask


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
    return redirect(request.POST.get('next', 'planner:task_list'))


@login_required
def task_start(request, pk):
    task = get_object_or_404(StudyTask, pk=pk, student=request.user)
    if request.method == 'POST' and task.status != StudyTask.STATUS_COMPLETED:
        task.status = StudyTask.STATUS_IN_PROGRESS
        _stamp_completion(task)
        task.save()
        messages.success(request, 'Task started.')
    return redirect(request.POST.get('next', 'planner:task_list'))


def get_today_plan(user):
    today = timezone.localdate()
    open_tasks = StudyTask.objects.filter(
        student=user, due_date__lte=today
    ).exclude(status=StudyTask.STATUS_COMPLETED).select_related(
        'subject', 'chapter', 'topic'
    ).order_by('-priority', 'due_date', '-created_at')
    completed_today = StudyTask.objects.filter(
        student=user,
        status=StudyTask.STATUS_COMPLETED,
        completed_at__date=today,
    ).select_related('subject', 'chapter', 'topic')
    open_minutes = sum(t.estimated_minutes for t in open_tasks)
    done_minutes = sum(t.estimated_minutes for t in completed_today)
    total_minutes = open_minutes + done_minutes
    if total_minutes:
        progress_percent = round(done_minutes * 100 / total_minutes)
    else:
        progress_percent = 0
    return {
        'date': today,
        'open_tasks': list(open_tasks),
        'completed_today': list(completed_today),
        'open_count': len(open_tasks),
        'done_count': len(completed_today),
        'open_minutes': open_minutes,
        'done_minutes': done_minutes,
        'total_minutes': total_minutes,
        'progress_percent': progress_percent,
        'next_task': open_tasks[0] if open_tasks else None,
    }


@login_required
def today_plan(request):
    return render(request, 'planner/today.html', get_today_plan(request.user))


@login_required
def session_start(request, task_pk):
    task = get_object_or_404(StudyTask, pk=task_pk, student=request.user)
    if request.method == 'POST':
        active = StudySession.objects.filter(
            student=request.user, ended_at__isnull=True
        ).first()
        if active is not None:
            messages.info(request, 'You already have an active session.')
            return redirect('planner:session_detail', pk=active.pk)
        session = StudySession.objects.create(
            student=request.user, task=task
        )
        messages.success(request, 'Study session started.')
        return redirect('planner:session_detail', pk=session.pk)
    return redirect('planner:today')


@login_required
def session_detail(request, pk):
    session = get_object_or_404(StudySession, pk=pk, student=request.user)
    form = StudySessionFinishForm(instance=session) if session.is_active else None
    return render(request, 'planner/session_detail.html', {
        'session': session, 'form': form,
    })


@login_required
def session_finish(request, pk):
    session = get_object_or_404(StudySession, pk=pk, student=request.user)
    if not session.is_active:
        return redirect('planner:session_detail', pk=session.pk)
    if request.method == 'POST':
        form = StudySessionFinishForm(request.POST, instance=session)
        if form.is_valid():
            session = form.save(commit=False)
            session.ended_at = timezone.now()
            session.full_clean()
            session.save()
            messages.success(request, 'Study session finished.')
            return redirect('planner:session_detail', pk=session.pk)
    else:
        form = StudySessionFinishForm(instance=session)
    return render(request, 'planner/session_detail.html', {
        'session': session, 'form': form,
    })


@login_required
def session_history(request):
    sessions = StudySession.objects.filter(
        student=request.user
    ).select_related('task', 'task__subject')
    return render(request, 'planner/session_history.html', {
        'sessions': sessions,
    })
