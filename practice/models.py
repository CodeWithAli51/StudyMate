from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Question(models.Model):
    TYPE_MCQ = 'mcq'
    TYPE_TRUE_FALSE = 'true_false'
    TYPE_CHOICES = [
        (TYPE_MCQ, 'MCQ'),
        (TYPE_TRUE_FALSE, 'True/False'),
    ]

    DIFFICULTY_EASY = 1
    DIFFICULTY_MEDIUM = 2
    DIFFICULTY_HARD = 3
    DIFFICULTY_CHOICES = [
        (DIFFICULTY_EASY, 'Easy'),
        (DIFFICULTY_MEDIUM, 'Medium'),
        (DIFFICULTY_HARD, 'Hard'),
    ]

    TRUE = 'True'
    FALSE = 'False'

    subject = models.ForeignKey(
        'academics.Subject',
        on_delete=models.CASCADE,
        related_name='questions',
    )
    chapter = models.ForeignKey(
        'academics.Chapter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questions',
    )
    topic = models.ForeignKey(
        'academics.Topic',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questions',
    )
    text = models.TextField()
    question_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default=TYPE_MCQ
    )
    options = models.JSONField(default=list, blank=True)
    correct_answer = models.CharField(max_length=500)
    explanation = models.TextField(blank=True)
    difficulty = models.IntegerField(
        choices=DIFFICULTY_CHOICES, default=DIFFICULTY_MEDIUM
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['subject', '-created_at']

    def __str__(self):
        return self.text[:80]

    def is_correct_answer(self, selected):
        return selected == self.correct_answer

    def clean(self):
        super().clean()
        if self.chapter and self.chapter.subject_id != self.subject_id:
            raise ValidationError(
                {'chapter': 'Chapter must belong to the selected subject.'}
            )
        if self.topic:
            if self.chapter and self.topic.chapter_id != self.chapter.pk:
                raise ValidationError(
                    {'topic': 'Topic must belong to the selected chapter.'}
                )
            if self.topic.chapter.subject_id != self.subject_id:
                raise ValidationError(
                    {'topic': 'Topic must belong to the selected subject.'}
                )
        if self.question_type == self.TYPE_MCQ:
            options = self.options or []
            if len(options) < 2:
                raise ValidationError(
                    {'options': 'MCQ questions need at least two options.'}
                )
            if self.correct_answer not in options:
                raise ValidationError(
                    {'correct_answer': 'Correct answer must be one of the options.'}
                )
        elif self.question_type == self.TYPE_TRUE_FALSE:
            if self.options:
                raise ValidationError(
                    {'options': 'True/False questions must not have options.'}
                )
            if self.correct_answer not in (self.TRUE, self.FALSE):
                raise ValidationError(
                    {'correct_answer': 'True/False answer must be True or False.'}
                )


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(
        'academics.Subject',
        on_delete=models.CASCADE,
        related_name='quizzes',
    )
    description = models.TextField(blank=True)
    questions = models.ManyToManyField(
        Question, through='QuizQuestion', related_name='quizzes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['subject', '-created_at']

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='quiz_questions'
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='quiz_questions'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['quiz', 'order', 'pk']
        constraints = [
            models.UniqueConstraint(
                fields=['quiz', 'question'], name='unique_question_per_quiz'
            )
        ]

    def __str__(self):
        return f"{self.quiz.title} — Q{self.order}: {self.question.text[:40]}"

    def clean(self):
        super().clean()
        if self.question_id and self.quiz_id:
            if self.question.subject_id != self.quiz.subject_id:
                raise ValidationError(
                    'Question must belong to the same subject as the quiz.'
                )


class QuizAttempt(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
    )
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='attempts'
    )
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.student} — {self.quiz.title} ({self.started_at:%Y-%m-%d})"

    @property
    def is_complete(self):
        return self.completed_at is not None

    @property
    def total_questions(self):
        return self.quiz.questions.count()

    @property
    def correct_count(self):
        return self.answers.filter(is_correct=True).count()

    @property
    def accuracy_percent(self):
        if not self.total_questions:
            return 0
        return round(self.correct_count * 100 / self.total_questions)


class AnswerAttempt(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt, on_delete=models.CASCADE, related_name='answers'
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answer_attempts'
    )
    selected_answer = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['attempt', 'answered_at']
        constraints = [
            models.UniqueConstraint(
                fields=['attempt', 'question'], name='unique_answer_per_attempt'
            )
        ]

    def __str__(self):
        mark = '✓' if self.is_correct else '✗'
        return f"{mark} {self.question.text[:40]}"

    def clean(self):
        super().clean()
        if self.question_id and self.attempt_id:
            quiz = self.attempt.quiz
            if not quiz.questions.filter(pk=self.question_id).exists():
                raise ValidationError(
                    {'question': 'Question is not part of this quiz.'}
                )
            if self.question.question_type == Question.TYPE_MCQ:
                if self.selected_answer not in (self.question.options or []):
                    raise ValidationError(
                        {'selected_answer': 'Selected answer is not a valid option.'}
                    )
            elif self.question.question_type == Question.TYPE_TRUE_FALSE:
                if self.selected_answer not in (Question.TRUE, Question.FALSE):
                    raise ValidationError(
                        {'selected_answer': 'Answer must be True or False.'}
                    )
            expected = self.question.is_correct_answer(self.selected_answer)
            if self.is_correct != expected:
                raise ValidationError(
                    {'is_correct': 'Correctness flag does not match the answer.'}
                )
