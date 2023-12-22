from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .gpt import generate_response
from django.utils.decorators import method_decorator
from django.views import View
from .models import ChatHistory
import json
from django.urls import reverse


def base(request):
  return render (request, 'base.html')

def SignupPage(request):
  if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')

        if pass1 == pass2:
            existing_user = User.objects.filter(username=uname).exists()
            if not existing_user:
                my_user = User.objects.create_user(username=uname, email=email, password=pass1)
                UserProfile.objects.create(user=my_user, firstname=firstname, lastname=lastname)
                return redirect('login')
            else:
                return render(request, 'signup.html', {'error_message': 'Username already exists'})
        else:
            print("Passwords do not match")
            return render(request, 'signup.html', {'error_message': 'Passwords do not match'})

  return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success (request, ('You were logged out.'))
    return redirect('base')

@login_required
def user_home(request):
    return render(request, 'home.html')

@login_required
def chatbot(request):
    return render (request, 'chatbot.html')

@csrf_exempt
def ask(request):
    if request.method == 'POST':
        user_input = request.POST.get('userInput')
        bot_response = generate_response(user_input)
        return JsonResponse({'bot_response': bot_response})
    return HttpResponse(status=400)

@method_decorator(csrf_exempt, name='dispatch')
class SaveChatView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Extract conversations from the JSON data
            conversations = data.get('conversations', [])

            # Save each conversation to the database
            for conversation in conversations:
                user_message = conversation.get('user_message', '')
                bot_message = conversation.get('bot_message', '')
                ChatHistory.objects.create(user_message=user_message, bot_message=bot_message)

            # You can add additional logic here if needed

            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'success': False, 'error': str(e)})

def get_saved_chat(request):
    # Retrieve the saved chat history from the database
    chat_history = ChatHistory.objects.all()

    return render(request, 'saved_chat.html', {'chat_history': chat_history})