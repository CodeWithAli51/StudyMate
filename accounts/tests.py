from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import StudentProfile

User = get_user_model()


class StudentProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice', password='testpass123'
        )

    def test_profile_created_on_user_creation(self):
        self.assertTrue(StudentProfile.objects.filter(user=self.user).exists())

    def test_default_study_minutes(self):
        profile = self.user.student_profile
        self.assertEqual(profile.preferred_daily_study_minutes, 60)

    def test_string_representation_defaults_to_username(self):
        profile = self.user.student_profile
        self.assertEqual(str(profile), 'alice')

    def test_string_representation_uses_display_name(self):
        profile = self.user.student_profile
        profile.display_name = 'Alice Smith'
        profile.save()
        self.assertEqual(str(profile), 'Alice Smith')


class StudentProfileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice', password='testpass123'
        )
        self.client.login(username='alice', password='testpass123')

    def test_profile_view_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_setup_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:profile_setup'))
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view_shows_profile(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Daily study goal')

    def test_profile_setup_creates_profile(self):
        self.user.student_profile.delete()
        response = self.client.post(
            reverse('accounts:profile_setup'),
            {
                'display_name': 'Alice Smith',
                'grade': '10',
                'board': 'Maharashtra SSC',
                'academic_year': '2026-27',
                'goal': 'Score 90%+',
                'preferred_daily_study_minutes': 120,
            },
        )
        self.assertEqual(response.status_code, 302)
        profile = StudentProfile.objects.get(user=self.user)
        self.assertEqual(profile.display_name, 'Alice Smith')
        self.assertEqual(profile.preferred_daily_study_minutes, 120)

    def test_profile_edit_updates_profile(self):
        response = self.client.post(
            reverse('accounts:profile_edit'),
            {
                'display_name': 'Alice Updated',
                'grade': '10',
                'board': 'Maharashtra SSC',
                'academic_year': '2026-27',
                'goal': 'Score 95%+',
                'preferred_daily_study_minutes': 90,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.student_profile.refresh_from_db()
        self.assertEqual(self.user.student_profile.display_name, 'Alice Updated')
        self.assertEqual(self.user.student_profile.goal, 'Score 95%+')
        self.assertEqual(self.user.student_profile.preferred_daily_study_minutes, 90)


class StudentProfilePermissionTests(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            username='alice', password='testpass123'
        )
        self.user_b = User.objects.create_user(
            username='bob', password='testpass123'
        )
        self.user_a.student_profile.display_name = 'Alice A'
        self.user_a.student_profile.save()
        self.user_a.student_profile.refresh_from_db()
        self.user_b.student_profile.display_name = 'Bob B'
        self.user_b.student_profile.save()

    def test_user_b_cannot_read_user_a_profile(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bob B')
        self.assertNotContains(response, 'Alice A')

    def test_profile_view_uses_own_profile_only(self):
        self.client.login(username='bob', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertContains(response, 'Bob B')
        self.assertNotContains(response, 'Alice A')
