from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academics.models import Subject
from planner.models import StudySession, StudyTask


class LandingViewTests(TestCase):
    def test_landing_page_renders(self):
        response = self.client.get(reverse('dashboard:landing'))
        self.assertEqual(response.status_code, 200)

    def test_landing_page_shows_marketing_content(self):
        response = self.client.get(reverse('dashboard:landing'))
        self.assertContains(response, 'StudyMate')
        self.assertContains(response, 'Know exactly what to study today')

    def test_authenticated_user_redirected_to_dashboard(self):
        user = get_user_model().objects.create_user(username='tester')
        self.client.force_login(user)
        response = self.client.get(reverse('dashboard:landing'))
        self.assertRedirects(response, reverse('dashboard:home'))


class DashboardHomeViewTests(TestCase):
    def test_dashboard_home_page_renders(self):
        user = get_user_model().objects.create_user(username='tester')
        self.client.force_login(user)
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)


class DashboardContentTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user(
            username='alice', password='testpass123'
        )
        self.bob = User.objects.create_user(
            username='bob', password='testpass123'
        )
        self.maths = Subject.objects.create(name='Mathematics')
        self.open_task = StudyTask.objects.create(
            student=self.alice,
            title='Alice open task',
            subject=self.maths,
            due_date=timezone.localdate(),
            estimated_minutes=30,
        )
        self.done_task = StudyTask.objects.create(
            student=self.alice,
            title='Alice done task',
            subject=self.maths,
            due_date=timezone.localdate(),
            estimated_minutes=30,
            status=StudyTask.STATUS_COMPLETED,
            completed_at=timezone.now(),
        )
        StudyTask.objects.create(
            student=self.bob,
            title='Bob secret task',
            subject=self.maths,
            due_date=timezone.localdate(),
        )

    def test_greeting_and_progress(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alice')
        self.assertContains(response, '50%')
        self.assertContains(response, 'Alice open task')
        self.assertContains(response, 'Next up')
        self.assertNotContains(response, 'Bob secret task')

    def test_recent_session_activity(self):
        session = StudySession.objects.create(
            student=self.alice, task=self.done_task
        )
        session.ended_at = timezone.now()
        session.confidence = StudySession.CONFIDENCE_GOOD
        session.save()
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertContains(response, 'Alice done task')
        self.assertContains(response, 'Good')

    def test_empty_state(self):
        StudyTask.objects.filter(student=self.alice).delete()
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertContains(response, 'Add a task')
        self.assertContains(response, 'Nothing here yet')

    def test_quick_actions_present(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertContains(response, reverse('planner:today'))
        self.assertContains(response, reverse('planner:task_create'))
        self.assertContains(response, reverse('planner:session_history'))

    def test_streak_shown(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertContains(response, '1 day')
