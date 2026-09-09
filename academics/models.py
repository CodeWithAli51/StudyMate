from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Chapter(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='chapters'
    )
    name = models.CharField(max_length=200)
    number = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['subject', 'order', 'number', 'name']
        unique_together = ['subject', 'number']

    def __str__(self):
        return f"{self.subject.name} — Ch {self.number}: {self.name}"


class Topic(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name='topics'
    )
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['chapter', 'order', 'name']
        unique_together = ['chapter', 'name']

    def __str__(self):
        return f"{self.chapter.subject.name} — {self.chapter.name} — {self.name}"
