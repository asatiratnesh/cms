from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone number must be entered in the format: '999999999'. Up to 10 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=10, blank=False)
    address = models.CharField(max_length=80, blank=False)
    city = models.CharField(max_length=30, blank=False)
    state = models.CharField(max_length=30, blank=False)
    country = models.CharField(max_length=30, blank=False)
    pincode = models.IntegerField(blank=True, null=True,)
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()



class ContentItem(models.Model):
    categories_choices = (
        ("technology", "Technology"),
        ("history", "History"),
        ("art", "Art"),
        ("food", "Food")
    )

    title = models.CharField(max_length=30, blank=False)
    body = models.CharField(max_length=300, blank=False)
    summary = models.CharField(max_length=60, blank=False)
    doc = models.FileField(db_index=True, upload_to='not_used', blank=True)
    categories = models.CharField(max_length=30,
        choices=categories_choices, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)

