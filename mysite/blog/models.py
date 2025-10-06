from django.db import models
from django.conf import settings



class Student(models.Model):
    name = models.CharField(max_length=100)
    age  = models.IntegerField()
    grade = models.CharField(max_length=10) 
    models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.age} - {self.grade}"
    


class Post(models.Model):
    title = models.CharField(max_length=100)
    context = models.TextField()
    post = models.FileField(upload_to='post/', null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='posts')

    class Meta:
        permissions = [
            ('publish_post','can publish post'),
        ]
    
    def __str__(self):
        return self.title



class Author(models.Model):
    author_name = models.CharField(max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    avata = models.FileField(upload_to='avata/', null=True, blank=True)


    def __str__(self):
        return self.author_name
    



#CHAT:
class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('private', 'private chat'),
        ('group', 'group chat')
    ]
    room_name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    room_members = models.ManyToManyField(Author, related_name='chat_rooms')
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default='private')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.room_name:
            return self.room_name or f'Room #{self.pk}'
        members = ', '.join([m.author_name for m in self.room_members.all()])
        return f'Private chat between: {members}'


class Message(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='messages')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    context = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.author}: {self.context[:50]}..."

    