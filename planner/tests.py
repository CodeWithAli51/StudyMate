from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from academics.models import Chapter, Subject, Topic

from .models import StudyTask

User = get_user_model()


class StudyTaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice', password='testpass123'
        )
        self.maths = Subject.objects.create(name='Mathematics')
        self.science = Subject.objects.create(name='Science')
        self.algebra = Chapter.objects.create(
            subject=self.maths, name='Algebra', number=1
        )
        self.quadratic = Topic.objects.create(
            chapter=self.algebra, name='Quadratic Equations'
        )

    def make_task(self, **kwargs):
        defaults = {
            'student': self.user,
            'title': 'Learn quadratic formula',
            'subject': self.maths,
        }
        defaults.update(kwargs)
        return StudyTask.objects.create(**defaults)

    def test_defaults(self):
        task = self.make_task()
        self.assertEqual(task.status, StudyTask.STATUS_TODO)
        self.assertEqual(task.task_type, StudyTask.TASK_LEARN)
        self.assertEqual(task.priority, StudyTask.PRIORITY_MEDIUM)
        self.assertEqual(task.estimated_minutes, 30)
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.completed_at)
        self.assertIsNotNone(task.created_at)

    def test_string_representation(self):
        self.assertEqual(str(self.make_task()), 'Learn quadratic formula')

    def test_task_visible_from_student(self):
        task = self.make_task()
        self.assertIn(task, self.user.study_tasks.all())

    def test_chapter_must_belong_to_subject(self):
        other_chapter = Chapter.objects.create(
            subject=self.science, name='Life Processes', number=1
        )
        task = StudyTask(
            student=self.user,
            title='Mismatch',
            subject=self.maths,
            chapter=other_chapter,
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_topic_must_belong_to_chapter(self):
        other_chapter = Chapter.objects.create(
            subject=self.maths, name='Geometry', number=2
        )
        task = StudyTask(
            student=self.user,
            title='Mismatch',
            subject=self.maths,
            chapter=other_chapter,
            topic=self.quadratic,
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_topic_must_belong_to_subject(self):
        physics_chapter = Chapter.objects.create(
            subject=self.science, name='Motion', number=1
        )
        physics_topic = Topic.objects.create(
            chapter=physics_chapter, name='Speed'
        )
        task = StudyTask(
            student=self.user,
            title='Mismatch',
            subject=self.maths,
            topic=physics_topic,
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_valid_hierarchy_passes_validation(self):
        task = StudyTask(
            student=self.user,
            title='Valid',
            subject=self.maths,
            chapter=self.algebra,
            topic=self.quadratic,
            task_type=StudyTask.TASK_PRACTICE,
            status=StudyTask.STATUS_IN_PROGRESS,
        )
        task.full_clean()
        task.save()
        self.assertEqual(task.chapter, self.algebra)
        self.assertEqual(task.topic, self.quadratic)

    def test_deleting_user_deletes_tasks(self):
        self.make_task()
        self.user.delete()
        self.assertEqual(StudyTask.objects.count(), 0)
