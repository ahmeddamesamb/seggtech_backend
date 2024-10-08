from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15, blank=True, null=True)  # Champ pour le numéro de téléphone
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Champ pour la photo de profil
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']  # Le champ 'nom' est requis lors de la création d'un utilisateur

    def __str__(self):
        return self.email


class Mesure(models.Model):
    temperature = models.FloatField(null=True)
    tds = models.FloatField(null=True)
    turbidite = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True)
    conductivite = models.FloatField(null=True)
    oxygene = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'Mesure du {self.timestamp}: Temperature: {self.temperature}, '
                f'TDS={self.tds}, Turbidite: {self.turbidite}, pH: {self.ph}, '
                f'Conductivite: {self.conductivite}, Oxygène: {self.oxygene}')
