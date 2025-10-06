from django.contrib import admin
from .models import Student, Post, Author, Room, Message



class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'grade')
    search_fields = ('name', 'age', 'grade')
    list_filter = ('name', 'age', 'grade')
admin.site.register(Student, StudentAdmin)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title')
    search_fields = ('author', 'title')



@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'author_name')
    search_fields = ('user__username', 'author_name')  



class MessageInline(admin.TabularInline):
    model = Message
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'room_type')
    search_fields = ('room_name', 'room_type')
    inlines = [MessageInline]



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'room', 'context', 'date')
    search_fields = ('author__author_name', 'room__room_name', 'content')
    list_filter = ('date',)


