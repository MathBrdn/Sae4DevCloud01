from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from .models import User
import asyncio
import nats
import json
from django.contrib.auth.hashers import check_password
from rest_framework.renderers import JSONRenderer
from .serializer import UserSerializer

def index(request):
    return render(request, "app/index.html")

def inscription(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        role_input = request.POST.get('role')
        User.objects.create(
            username=username_input,
            password=make_password(password_input),
            role=role_input
        )
        return HttpResponseRedirect('/app/login') 
    return render(request, 'app/inscription.html')

async def notifier_connexion_nats(username, role):
    nc = await nats.connect("nats://nats:4222")
    payload = {"username": username, "role": role}
    sujet = f"auth.{role.lower()}"
    await nc.publish(sujet, json.dumps(payload).encode())
    await nc.flush()
    await nc.close()

def login(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        try:
            user = User.objects.get(username=username_input)
            if check_password(password_input, user.password):
                asyncio.run(notifier_connexion_nats(user)) 
                if user.role == User.Role.ADMIN:
                    return redirect('http://192.168.178.13:8002')
                else:
                    return redirect(f'http://192.168.178.13:8003/app/{user.id}/')
            else:
                error = "Mot de passe incorrect"
        except User.DoesNotExist:
            error = "Utilisateur introuvable"
        return render(request, 'login.html', {'error': error})    
    return render(request, 'app/login.html')

async def notifier_connexion_nats(user_instance):
    nc = await nats.connect("nats://nats:4222")
    serializer = UserSerializer(user_instance)
    json_data = JSONRenderer().render(serializer.data)
    sujet = f"auth.{user_instance.role.lower()}"
    await nc.publish(sujet, json_data)
    
    await nc.flush()
    await nc.close()