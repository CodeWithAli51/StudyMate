from django.shortcuts import render, get_object_or_404

from .models import Subject, Chapter, Topic


def index(request):
    return render(request, 'academics/index.html', {
        'subjects': Subject.objects.all(),
    })


def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'academics/subject_detail.html', {
        'subject': subject,
        'chapters': subject.chapters.all(),
    })


def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    return render(request, 'academics/chapter_detail.html', {
        'chapter': chapter,
        'topics': chapter.topics.all(),
    })


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, 'academics/topic_detail.html', {
        'topic': topic,
    })
