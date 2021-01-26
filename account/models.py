from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


class AccountManager(BaseUserManager):
    def create_user(self, email, displayname, password=None):
        if not email:
            raise ValueError('Email field is required.')
        if not displayname:
            raise ValueError('Displayname field is required.')
        user = self.model (
            email=self.normalize_email(email),
            displayname=displayname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, displayname, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            displayname=displayname,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    displaynameValidator = RegexValidator('^[-0-9a-zA-Z\u0622\u0627\u0628\u067E\u062A-\u062C\u0686\u062D-\u0632\u0698\u0633-\u063A\u0641\u0642\u06A9\u06AF\u0644-\u0648\u06CC\u06F0-\u06F9 ]*$', 'invalid format.')

    email = models.EmailField(max_length=256, unique=True)
    displayname = models.CharField(max_length=20, validators=[displaynameValidator])
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['displayname']

    objects = AccountManager()

    def __str__(self):
        return self.displayname


class ConfirmationCode(models.Model):
    code = models.IntegerField()
    email = models.EmailField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)
