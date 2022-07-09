from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from . models import *
from . forms import *
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def loginpage(request):
    page = 'login'
    if request.user.is_authenticated: 
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else: 
            messages.info(request, 'Email or Password is incorrect')

    context = {'page':page}
    return render(request, 'dipole/login_register.html', context)



def logoutuser(request):
    logout(request)
    return redirect('home')

def registeruser(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'An Unknown error occured! Try Again! ')

    return render(request, 'dipole/login_register.html', {'form': form})


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q)|
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
                                )
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms,'topics':topics,'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'dipole/home.html', context)

@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
        user = request.user,
        room = room,
        body=request.POST.get('message')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room,'room_messages': room_messages,'participants':participants, }
    return render(request, 'dipole/room.html', context)


def userprofile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context ={'user': user, 'rooms':rooms, 'room_messages': room_messages, 'topics':topics}
    return render(request, 'dipole/profile.html', context)


# def join_group(request,pk):
#     room = Room.objects.get(id=pk)

#     if request.method == 'POST': 
#         room.participants.add(request.user)
#         room.save()
#         return redirect('group'+str(pk))
#     else: 
#         return redirect('home')


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description= request.POST.get('description')
        )
        return redirect('/')

    context = {'form':form, 'topics':topics}
    return render(request, 'dipole/room_form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are devil! GO away')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('home')

    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'dipole/room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are devil! GO away')

    if request.method == 'POST':
        room.delete()
        return redirect('/')

    return render(request, 'dipole/delete.html', {'obj':room})

@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are devil! GO away')

    if request.method == 'POST':
        message.delete()
        return redirect('/')

    return render(request, 'dipole/delete.html', {'obj':message})


@login_required(login_url='login')
def updateuser(request):
    user = request.user
    form = userForm(instance=user)

    if request.method == 'POST':
        form = userForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form': form}
    return render(request, 'dipole/update_user.html', context)

@login_required(login_url='login')
def topicspage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics':topics}
    return render(request, 'dipole/topics.html', context)

@login_required(login_url='login')
def activitypage(request):
    room_messages = Message.objects.all()[0:5]
    context = {'room_messages':room_messages}
    return render(request, 'dipole/activity.html', context)


