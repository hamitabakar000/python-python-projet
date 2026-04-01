# teacher/models.py
from django.db import models


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    joining_date = models.DateField()
    qualification = models.CharField(max_length=200)
    experience = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(
        'department.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teachers'
    )
    address = models.TextField(blank=True)
    teacher_image = models.ImageField(upload_to='teachers/', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"
