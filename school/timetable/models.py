# timetable/models.py
from django.db import models


class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    class_name = models.CharField(max_length=50)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey(
        'subject.Subject',
        on_delete=models.CASCADE,
        related_name='timetable_entries'
    )
    teacher = models.ForeignKey(
        'teacher.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='timetable_entries'
    )
    room = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.class_name} - {self.day} - {self.subject.name} ({self.start_time}-{self.end_time})"

    class Meta:
        ordering = ['day', 'start_time']
