from datetime import datetime
from wsgiref.validate import validator
from django.db import models
from django.forms import ChoiceField
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.exceptions import ValidationError

def file_size(value): # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size >= limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')

class MyUserManager(BaseUserManager):
    def create_user(self, age=None, description=None, telephone=None, email=None, gender=None, password=None, time_create=datetime.now):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            age=age,
            description=description,
            telephone=telephone,
            email=MyUserManager.normalize_email(email),
            gender=gender,       
            time_create=time_create,    
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, is_staff='False', age='23', description='This is Student', telephone='+78005553535', email='', gender='M', password=None, time_create=datetime.now):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        u = self.create_user(
            age=age,
            description=description,
            telephone=telephone,
            email=MyUserManager.normalize_email(email),
            gender=gender,        
            password=password,
        )
        u.is_admin = True
        u.save(using=self._db)
        return u

class UserNet(AbstractBaseUser):
    age = models.PositiveIntegerField(default=0, verbose_name='Возраст')
    description = models.TextField(max_length=500, verbose_name="Информация о себе")
    telephone = PhoneNumberField(max_length=12, unique=True, blank=True, verbose_name='Номер телефона')
    email = models.EmailField(unique=True, blank=True, verbose_name='Электронная почта')
    gender = models.CharField(verbose_name="Пол", choices=( ('M', 'Male'),('F', 'Female'),('O', 'Other')), default="M", max_length=1)
    time_create = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['telephone']
 

    objects = MyUserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class PostNet(models.Model):
    author = models.ForeignKey('UserNet', on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(max_length=500, blank=True, verbose_name='Текст статьи')
    photo = models.ImageField(upload_to='images/', verbose_name='Изображение', validators=[file_size])
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    
    def __str__(self):
        return self.title
    
    
class PostImages(models.Model):
    post = models.ForeignKey('PostNet', on_delete=models.CASCADE, verbose_name='Изображение')
    image = models.ImageField(upload_to='images/shots/', validators=[file_size])
    description = models.TextField(max_length=30, blank=False)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.description

