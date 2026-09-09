from django.test import TestCase
from .models import Subject, Chapter, Topic


class AcademicStructureTests(TestCase):
    def test_subject_str(self):
        s = Subject.objects.create(name='Mathematics', code='MATH')
        self.assertEqual(str(s), 'Mathematics')

    def test_chapter_with_subject(self):
        s = Subject.objects.create(name='Science')
        ch = Chapter.objects.create(subject=s, name='Life Processes', number=1)
        self.assertIn(ch, s.chapters.all())
        self.assertEqual(str(ch), 'Science — Ch 1: Life Processes')

    def test_topic_with_chapter(self):
        s = Subject.objects.create(name='History')
        ch = Chapter.objects.create(subject=s, name='Ancient', number=2)
        t = Topic.objects.create(chapter=ch, name='Indus Valley', order=1)
        self.assertIn(t, ch.topics.all())
        self.assertTrue(str(t).startswith('History'))

    def test_unique_subject_name(self):
        Subject.objects.create(name='Unique')
        with self.assertRaises(Exception):
            Subject.objects.create(name='Unique')

    def test_chapter_unique_number_per_subject(self):
        s = Subject.objects.create(name='Geo')
        Chapter.objects.create(subject=s, name='A', number=1)
        with self.assertRaises(Exception):
            Chapter.objects.create(subject=s, name='B', number=1)
