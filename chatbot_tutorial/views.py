from chatbot_tutorial.models import JokeCount
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render


def chat(request):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)

def joke_list(request):
    all_jokes = JokeCount.objects.all() 
    users = all_jokes.distinct('user').values_list('user', flat=True)
    
    jokes = []
    for (index, user) in enumerate(users):
        data = {}
        data["SlNo"] = index+1
        data["User"] = user
        data["Dumb"] = all_jokes.filter(user=user, joke_word="dumb").count()
        data["Fat"] = all_jokes.filter(user=user, joke_word="fat").count()
        data["Stupid"] = all_jokes.filter(user=user, joke_word="stupid").count()
        jokes.append(data)
    return render(request, 'chatbot_tutorial/joke_list.html', {'jokes': jokes})


def respond_to_websockets(joke_type):
    jokes = {
     'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
     'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
     'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] 
     }  

    result_message = {
        'type': 'text'
    }
    if joke_type == 'fat':
        result_message['text'] = random.choice(jokes['fat'])
    
    elif joke_type == 'stupid':
        result_message['text'] = random.choice(jokes['stupid'])
    
    elif joke_type == 'dumb':
        result_message['text'] = random.choice(jokes['dumb'])

    return result_message
    