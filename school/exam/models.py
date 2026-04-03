# exam/models.py
from django.db import models


class Exam(models.Model):
    name = models.CharField(max_length=100)
    exam_date = models.DateField()
    subject = models.ForeignKey(
        'subject.Subject',
        on_delete=models.CASCADE,
        related_name='exams'
    )
    class_name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_marks = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.name} - {self.subject.name} ({self.exam_date})"

    class Meta:
        ordering = ['exam_date', 'start_time']


class ExamResult(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('B+', 'B+'), ('B', 'B'),
        ('C+', 'C+'), ('C', 'C'), ('D', 'D'), ('F', 'F'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(
        'student.Student',
        on_delete=models.CASCADE,
        related_name='exam_results'
    )
    marks_obtained = models.IntegerField()
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES, blank=True)
    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Auto-calculate grade
        try:
            total_marks = int(self.exam.total_marks)
            marks_obtained = int(self.marks_obtained)
            if total_marks > 0:
                percentage = (marks_obtained / total_marks) * 100
                if percentage >= 90:
                    self.grade = 'A+'
                elif percentage >= 80:
                    self.grade = 'A'
                elif percentage >= 70:
                    self.grade = 'B+'
                elif percentage >= 60:
                    self.grade = 'B'
                elif percentage >= 50:
                    self.grade = 'C+'
                elif percentage >= 40:
                    self.grade = 'C'
                elif percentage >= 30:
                    self.grade = 'D'
                else:
                    self.grade = 'F'
        except (ValueError, TypeError):
            # Fallback if marks are not numbers
            self.grade = 'F'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.marks_obtained}/{self.exam.total_marks}"

    class Meta:
        unique_together = ['exam', 'student']
