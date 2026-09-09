from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

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


class StudyTaskViewTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            username='alice', password='testpass123'
        )
        self.bob = User.objects.create_user(
            username='bob', password='testpass123'
        )
        self.maths = Subject.objects.create(name='Mathematics')
        self.science = Subject.objects.create(name='Science')
        self.task = StudyTask.objects.create(
            student=self.alice,
            title='Alice task',
            subject=self.maths,
        )
        self.task_data = {
            'title': 'New task',
            'subject': self.maths.pk,
            'task_type': StudyTask.TASK_PRACTICE,
            'estimated_minutes': 45,
            'priority': StudyTask.PRIORITY_HIGH,
            'status': StudyTask.STATUS_TODO,
        }

    def test_list_requires_login(self):
        response = self.client.get(reverse('planner:task_list'))
        self.assertEqual(response.status_code, 302)

    def test_create_requires_login(self):
        response = self.client.post(
            reverse('planner:task_create'), self.task_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(StudyTask.objects.count(), 1)

    def test_list_shows_own_tasks_only(self):
        StudyTask.objects.create(
            student=self.bob, title='Bob task', subject=self.science
        )
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('planner:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice task')
        self.assertNotContains(response, 'Bob task')

    def test_list_empty_state(self):
        self.task.delete()
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('planner:task_list'))
        self.assertContains(response, 'No study tasks yet')

    def test_create_task(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(
            reverse('planner:task_create'), self.task_data
        )
        self.assertEqual(response.status_code, 302)
        task = StudyTask.objects.get(title='New task')
        self.assertEqual(task.student, self.alice)
        self.assertEqual(task.priority, StudyTask.PRIORITY_HIGH)

    def test_update_task(self):
        self.client.login(username='alice', password='testpass123')
        data = dict(self.task_data, title='Updated title')
        response = self.client.post(
            reverse('planner:task_update', args=[self.task.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated title')

    def test_delete_task(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(
            reverse('planner:task_delete', args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(StudyTask.objects.filter(pk=self.task.pk).exists())

    def test_complete_task(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(
            reverse('planner:task_complete', args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, StudyTask.STATUS_COMPLETED)
        self.assertIsNotNone(self.task.completed_at)

    def test_filter_by_subject(self):
        StudyTask.objects.create(
            student=self.alice, title='Science task', subject=self.science
        )
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(
            reverse('planner:task_list'), {'subject': self.science.pk}
        )
        self.assertContains(response, 'Science task')
        self.assertNotContains(response, 'Alice task')

    def test_filter_by_status(self):
        StudyTask.objects.create(
            student=self.alice,
            title='Done task',
            subject=self.maths,
            status=StudyTask.STATUS_COMPLETED,
        )
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(
            reverse('planner:task_list'),
            {'status': StudyTask.STATUS_COMPLETED},
        )
        self.assertContains(response, 'Done task')
        self.assertNotContains(response, 'Alice task')

    def test_cannot_edit_other_user_task(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.post(
            reverse('planner:task_update', args=[self.task.pk]),
            dict(self.task_data, title='Hijacked'),
        )
        self.assertEqual(response.status_code, 404)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Alice task')

    def test_cannot_delete_other_user_task(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.post(
            reverse('planner:task_delete', args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(StudyTask.objects.filter(pk=self.task.pk).exists())

    def test_cannot_complete_other_user_task(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.post(
            reverse('planner:task_complete', args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 404)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, StudyTask.STATUS_TODO)
