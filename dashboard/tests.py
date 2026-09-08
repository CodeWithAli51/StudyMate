from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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
