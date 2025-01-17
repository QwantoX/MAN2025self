from django.db import models

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class TeachingAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='assignments')

    class Meta:
        unique_together = ('teacher', 'subject', 'school_class')  # унікальність

    def __str__(self):
        return f"{self.teacher.name} викладає {self.subject.name} у {self.school_class.name}"
