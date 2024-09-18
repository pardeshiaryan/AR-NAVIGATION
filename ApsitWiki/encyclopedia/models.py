from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Page(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

class UserManager(BaseUserManager):
    def create_user(self, MoodleId, password=None):
        if not MoodleId:
            raise ValueError('Users must have a MoodleId')
        user = self.model(MoodleId=MoodleId)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, MoodleId, password):
        user = self.create_user(MoodleId, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserCustom(AbstractBaseUser):
    MoodleId = models.CharField(max_length=50, unique=True)
    Password = models.CharField(max_length=50)

    objects = UserManager()

    USERNAME_FIELD = 'MoodleId'

    def __str__(self):
        return self.MoodleId
