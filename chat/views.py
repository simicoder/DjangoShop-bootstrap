from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import json
from chat.models import Room

@login_required
def index(request):
	chats1 = list(Room.objects.filter(user_1=request.user))
	chats2 = list(Room.objects.filter(user_2=request.user))
	return render(request, 'chat/room.html', {
		'chats1': chats1,
		'chats2': chats2,
		})

@login_required
def room(request, room_name):
	chats1 = list(Room.objects.filter(user_1=request.user))
	chats2 = list(Room.objects.filter(user_2=request.user))

	return render(request, 'chat/room.html', {
		'chats1': chats1,
		'chats2': chats2,
		'room_name_json': mark_safe(json.dumps(room_name)),
		'username': mark_safe(json.dumps(request.user.username)),
	})