from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator

from .validators import validate_username

class User(AbstractUser):
    REQUIRED_FIELDS = []
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        validators=[validate_username],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    password = models.CharField(max_length=128, validators=[MinLengthValidator(6, message="password length MUST be 6 characters or more")])
    
    name = models.CharField(max_length=150, blank=True)
    phone_number = PhoneNumberField(blank=True)
    
    
    
    first_name = None
    last_name = None
    last_login = None
