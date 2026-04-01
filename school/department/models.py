# department/models.py
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    head = models.ForeignKey(
        'teacher.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_department'
    )
    description = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
