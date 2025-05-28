# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import Favorites

# @receiver(post_save, sender=User)
# def create_favorites(sender, instance, created, **kwargs):
#     if created:
#         Favorites.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_favorites(sender, instance, **kwargs):
#     instance.Favorites.save()