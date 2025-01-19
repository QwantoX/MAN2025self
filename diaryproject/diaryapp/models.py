from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SchoolClass(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser, PermissionsMixin):  #PermissionsMixin
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
    assigned_subjects = models.ManyToManyField(Subject, blank=True)
    assigned_classes = models.ManyToManyField(SchoolClass, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        """
        Чи має користувач конкретне право.
        """
        return self.is_superuser

    def has_module_perms(self, app_label):
        """
        Чи має користувач доступ до модулів програми.
        """
        return self.is_superuser
