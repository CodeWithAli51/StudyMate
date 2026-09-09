from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from academics.models import Chapter, Subject, Topic

from .models import (
    AnswerAttempt,
    Question,
    Quiz,
    QuizAttempt,
    QuizQuestion,
)

User = get_user_model()


class QuestionModelTests(TestCase):
    def setUp(self):
        self.maths = Subject.objects.create(name='Mathematics')
        self.science = Subject.objects.create(name='Science')
        self.algebra = Chapter.objects.create(
            subject=self.maths, name='Algebra', number=1
        )
        self.quadratic = Topic.objects.create(
            chapter=self.algebra, name='Quadratic Equations'
        )

    def make_mcq(self, **kwargs):
        defaults = {
            'subject': self.maths,
            'chapter': self.algebra,
            'topic': self.quadratic,
            'text': 'What is 2 + 2?',
            'question_type': Question.TYPE_MCQ,
            'options': ['3', '4', '5'],
            'correct_answer': '4',
            'explanation': 'Basic addition.',
            'difficulty': Question.DIFFICULTY_EASY,
        }
        defaults.update(kwargs)
        return Question(**defaults)

    def test_valid_mcq(self):
        question = self.make_mcq()
        question.full_clean()
        question.save()
        self.assertEqual(question.difficulty, Question.DIFFICULTY_EASY)
        self.assertTrue(question.is_correct_answer('4'))
        self.assertFalse(question.is_correct_answer('3'))

    def test_valid_true_false(self):
        question = Question(
            subject=self.maths,
            text='The square of 5 is 25.',
            question_type=Question.TYPE_TRUE_FALSE,
            correct_answer=Question.TRUE,
        )
        question.full_clean()
        question.save()
        self.assertTrue(question.is_correct_answer('True'))

    def test_mcq_needs_two_options(self):
        question = self.make_mcq(options=['only'])
        with self.assertRaises(ValidationError):
            question.full_clean()

    def test_mcq_correct_answer_must_be_option(self):
        question = self.make_mcq(correct_answer='7')
        with self.assertRaises(ValidationError):
            question.full_clean()

    def test_true_false_rejects_options(self):
        question = Question(
            subject=self.maths,
            text='Is this valid?',
            question_type=Question.TYPE_TRUE_FALSE,
            options=['True', 'False'],
            correct_answer=Question.TRUE,
        )
        with self.assertRaises(ValidationError):
            question.full_clean()

    def test_true_false_rejects_other_answers(self):
        question = Question(
            subject=self.maths,
            text='Is this valid?',
            question_type=Question.TYPE_TRUE_FALSE,
            correct_answer='Maybe',
        )
        with self.assertRaises(ValidationError):
            question.full_clean()

    def test_question_chapter_must_match_subject(self):
        physics = Chapter.objects.create(
            subject=self.science, name='Motion', number=1
        )
        question = self.make_mcq(chapter=physics, topic=None)
        with self.assertRaises(ValidationError):
            question.full_clean()

    def test_question_topic_must_match_chapter(self):
        geometry = Chapter.objects.create(
            subject=self.maths, name='Geometry', number=2
        )
        question = self.make_mcq(topic=self.quadratic)
        question.chapter = geometry
        with self.assertRaises(ValidationError):
            question.full_clean()


class QuizRelationTests(TestCase):
    def setUp(self):
        self.maths = Subject.objects.create(name='Mathematics')
        self.science = Subject.objects.create(name='Science')
        self.quiz = Quiz.objects.create(title='Algebra Quiz', subject=self.maths)
        self.q1 = Question.objects.create(
            subject=self.maths,
            text='What is 2 + 2?',
            question_type=Question.TYPE_MCQ,
            options=['3', '4'],
            correct_answer='4',
        )
        self.q2 = Question.objects.create(
            subject=self.maths,
            text='The square of 3 is 9.',
            question_type=Question.TYPE_TRUE_FALSE,
            correct_answer=Question.TRUE,
        )

    def test_add_questions_in_order(self):
        QuizQuestion.objects.create(quiz=self.quiz, question=self.q2, order=2)
        QuizQuestion.objects.create(quiz=self.quiz, question=self.q1, order=1)
        self.assertEqual(
            list(self.quiz.questions.order_by('quiz_questions__order')),
            [self.q1, self.q2],
        )

    def test_duplicate_question_rejected(self):
        QuizQuestion.objects.create(quiz=self.quiz, question=self.q1)
        with self.assertRaises(IntegrityError):
            QuizQuestion.objects.create(quiz=self.quiz, question=self.q1)

    def test_cross_subject_question_rejected(self):
        other = Question.objects.create(
            subject=self.science,
            text='Water boils at 100°C.',
            question_type=Question.TYPE_TRUE_FALSE,
            correct_answer=Question.TRUE,
        )
        relation = QuizQuestion(quiz=self.quiz, question=other)
        with self.assertRaises(ValidationError):
            relation.full_clean()


class AttemptTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            username='alice', password='testpass123'
        )
        self.maths = Subject.objects.create(name='Mathematics')
        self.quiz = Quiz.objects.create(title='Algebra Quiz', subject=self.maths)
        self.q1 = Question.objects.create(
            subject=self.maths,
            text='What is 2 + 2?',
            question_type=Question.TYPE_MCQ,
            options=['3', '4'],
            correct_answer='4',
        )
        self.q2 = Question.objects.create(
            subject=self.maths,
            text='The square of 3 is 9.',
            question_type=Question.TYPE_TRUE_FALSE,
            correct_answer=Question.TRUE,
        )
        QuizQuestion.objects.create(quiz=self.quiz, question=self.q1, order=1)
        QuizQuestion.objects.create(quiz=self.quiz, question=self.q2, order=2)
        self.attempt = QuizAttempt.objects.create(
            student=self.alice, quiz=self.quiz
        )

    def answer(self, question, selected, correct):
        answer = AnswerAttempt(
            attempt=self.attempt,
            question=question,
            selected_answer=selected,
            is_correct=correct,
        )
        answer.full_clean()
        answer.save()
        return answer

    def test_correct_and_incorrect_answers(self):
        self.answer(self.q1, '4', True)
        self.answer(self.q2, 'False', False)
        self.assertEqual(self.attempt.correct_count, 1)
        self.assertEqual(self.attempt.total_questions, 2)
        self.assertEqual(self.attempt.accuracy_percent, 50)

    def test_wrong_correctness_flag_rejected(self):
        with self.assertRaises(ValidationError):
            self.answer(self.q1, '4', False)

    def test_invalid_option_rejected(self):
        with self.assertRaises(ValidationError):
            self.answer(self.q1, 'Not an option', False)

    def test_question_outside_quiz_rejected(self):
        outsider = Question.objects.create(
            subject=self.maths,
            text='Outsider?',
            question_type=Question.TYPE_TRUE_FALSE,
            correct_answer=Question.FALSE,
        )
        with self.assertRaises(ValidationError):
            self.answer(outsider, 'False', True)

    def test_duplicate_answer_rejected(self):
        self.answer(self.q1, '4', True)
        with self.assertRaises(IntegrityError):
            AnswerAttempt.objects.create(
                attempt=self.attempt,
                question=self.q1,
                selected_answer='4',
                is_correct=True,
            )

    def test_attempts_belong_to_student(self):
        bob = User.objects.create_user(username='bob', password='testpass123')
        bob_attempt = QuizAttempt.objects.create(student=bob, quiz=self.quiz)
        self.assertIn(self.attempt, self.alice.quiz_attempts.all())
        self.assertNotIn(self.attempt, bob.quiz_attempts.all())
        self.assertIn(bob_attempt, bob.quiz_attempts.all())

    def test_deleting_user_deletes_attempts(self):
        self.answer(self.q1, '4', True)
        self.alice.delete()
        self.assertEqual(QuizAttempt.objects.count(), 0)
        self.assertEqual(AnswerAttempt.objects.count(), 0)
