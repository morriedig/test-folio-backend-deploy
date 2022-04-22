from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

DISCOUNT_CODE_TYPES_CHOICES = [
    ("percent", "Percentage-based"),
    ("value", "Value-based"),
]


# Create your models here
class MyUserManager(BaseUserManager):
    def create_user(self, account, username, email, id_number, password=None):
        """
        Creates and saves a User with the given account, username, email, id number and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            id_number=id_number,
            account=account,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, account, username, email, id_number, password=None):
        """
        Creates and saves a superuser with the given account, username, email, id number and password.
        """
        user = self.create_user(email=email, password=password, id_number=id_number, account=account, username=username)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    id_number = models.CharField(max_length=10, unique=True)
    account = models.CharField(max_length=30, unique=True)
    username = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = "account"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.account

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
