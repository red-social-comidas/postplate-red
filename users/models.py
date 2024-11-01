from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from roles.models import Role
from django.db import models
import uuid
import cloudinary
import cloudinary.uploader
import cloudinary.models


def blog_thumbnail_directory(instance, filename=None):
    return f'blog_thumbnails/{instance.id}/{filename}'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser with email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    images = models.URLField(max_length=500, blank=True, null=True)
    image_public_id = models.CharField(max_length=100, blank=True, null=True)

    verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True, default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_thumbnail(self):
        """
        Retorna la URL de la imagen de perfil del usuario.
        """
        return self.images if self.images else ''

    def get_role(self):
        """
        Retorna el rol asignado al usuario. Si no tiene rol, devuelve 'sin rol definido'.
        """
        if hasattr(self, 'role') and self.role:
            return self.role.name
        return 'sin rol definido'
