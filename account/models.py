from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User



# Custom user manager
class MyAccountManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have a username!")

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Own custom user model
class Account(AbstractBaseUser):

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    profile_pic = models.ImageField(null=True, default="default.png")

    categoryTech = models.BooleanField( default=True)
    categoryPolitics = models.BooleanField( default=False)
    categorySport = models.BooleanField( default=False)

    DoB = models.CharField(default=True, max_length=30)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    # Referrences the account manager
    objects = MyAccountManager()

    # Whenever we print an account object to a template, display the username
    def __str__(self):
        return self.username

    # Required functions for custom users
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

