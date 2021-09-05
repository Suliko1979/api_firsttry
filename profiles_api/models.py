from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserProfileManager(BaseUserManager):

    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have email address!')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff=True

        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represent a user profile inside our system"""
    email = models.EmailField(max_length=255, unique=True, verbose_name='Емейл')
    name = models.CharField(max_length=250, verbose_name='Имя')
    is_active = models.BooleanField(default=True, verbose_name='Активен?')
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get a full name of the user"""
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class ProfileFeedItem(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text

