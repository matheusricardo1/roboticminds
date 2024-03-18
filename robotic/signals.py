from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import RoboticUser
import os

@receiver(pre_save, sender=RoboticUser)
def rename_profile_picture(sender, instance, **kwargs):
    if instance.profile_picture:
        username = slugify(instance.username)
        ext = os.path.splitext(instance.profile_picture.name)
        ext = ext[-1]
        ext = ext.replace('.','')
        file_ext_name = ext.upper()
        instance.profile_picture.name = f"{file_ext_name}/{username}_profile_picture.{ext}"
