# from django.db import models

# # Create your models here.

# class Teacher(models.Model):
#     name = models.CharField(max_length=30)

#     def __str__(self):
#         return f"ID: {self.id}, Teacher: {self.name}"

# class Subject(models.Model):
#     name = models.CharField(max_length=30)

#     def __str__(self):
#         return f"ID: {self.id}, Subject: {self.name}"

# class Class(models.Model):
#     name = models.CharField(max_length=10)

#     def __str__(self):
#         return f"ID: {self.id}, Class: {self.name}"

# class TeachingAssignment(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignments')
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
#     school_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='assignments')

#     class Meta:
#         unique_together = ('teacher', 'subject', 'school_class')  # унікальність

#     def __str__(self):
#         return f"ID: {self.id}, {self.teacher.name} викладає {self.subject.name} у {self.school_class.name}"


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
