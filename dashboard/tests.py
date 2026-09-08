from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_base_template(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertContains(response, 'StudyMate')
