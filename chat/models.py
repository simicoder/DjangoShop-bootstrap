from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404

User = get_user_model()

class Message(models.Model):
	room = models.ForeignKey('chat.Room', on_delete=models.CASCADE)
	author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
	content = models.TextField(max_length=400)
	timestamp = models.DateTimeField(auto_now_add=True)
	read = models.BooleanField(default=False)

	def __str__(self):
		return self.author.username

	def last_20_messages(room_name_mod, first_mes, last_mes):
		return Message.objects.filter(room=get_object_or_404(Room, room_name=room_name_mod)).order_by('-timestamp').all()[first_mes:last_mes]

class Room(models.Model):
	room_name = models.CharField(max_length=50)
	user_1 = models.ForeignKey(User, related_name='user_1', on_delete=models.CASCADE)
	user_2 = models.ForeignKey(User, related_name='user_2', on_delete=models.CASCADE)

	def __str__(self):
		return self.room_name