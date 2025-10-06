from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post, Author
import os



@receiver(post_delete, sender=Post)
def delete_file_on_post_delete(sender, instance, **kwargs):
    if instance.post:
        instance.post.delete(save=False)



@receiver(pre_save, sender = Post)
def delete_file_on_post_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_post = Post.objects.get(pk = instance.pk)
    except Post.DoesNotExist:
        return
    
    if old_post.post and old_post.post != instance.post:
        if os.path.isfile(old_post.post.path):
            os.remove(old_post.post.path)



@receiver(post_save, sender=User)
def create_author_for_new_user(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance, author_name=instance.username)


