# holiday/models.py
from django.db import models


class Holiday(models.Model):
    HOLIDAY_TYPES = [
        ('Public', 'Public Holiday'),
        ('School', 'School Holiday'),
        ('Religious', 'Religious Holiday'),
        ('National', 'National Holiday'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    holiday_type = models.CharField(max_length=20, choices=HOLIDAY_TYPES, default='Public')

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"

    class Meta:
        ordering = ['start_date']
