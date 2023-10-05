from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from . import trainer
import re

from django.utils import timezone


openai_api_key = trainer.api_key() #"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"
openai.api_key = openai_api_key


# IA QUESTION SIMILARITY CHECKER
def similarity_ai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": '''you are a very very layperson, you are more human. you are cutomers srevice person and you are asked questions which you\'d check if the relate to or are simillar to any of the listed questions below. you respond with the exact question that the customers question is related or similar only the question nothing else attached, reply with just the qustion please remove numbering and if there are non related of similar you simpple respond with NO.
QUESTIONS
Is the cremation of my loved one complete?
What is the status of the death certificates?
When will the cremation be complete?
Can I order more death certificates?
Can I change the urn that I ordered?
Can I schedule an appointment to pick up?'''
             },

            {"role": "user", "content": message},
        ]
    )

    # print(response)
    answer = response.choices[0].message.content.strip()
    return answer

# EMAIL REQUEST
def email_reuests(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": trainer.email_question()},
            {"role": "user", "content": message},
        ]
    )

    # print(response)
    answer = response.choices[0].message.content.strip()
    return answer


# AI RESPONSE FORM KRAMER WEBSITE
def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": trainer.texax_info()},
            {"role": "user", "content": message},
        ]
    )

    # print(response)
    answer = response.choices[0].message.content.strip()
    return answer

def is_valid_email(email):
    # Define a regular expression pattern for a basic email format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Use re.match() to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False

# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        # lst = re.findall('\S+@\S+', s)
        try:
            match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', message)
            email = match.group(0)
            print(match.group(0))
        except:
            email = "blank"

        if is_valid_email(email):
            print(f"{email} is a valid email address.")
            response = 'Monday'
        else:
            print(f"{email} is not a valid email address.")

            new_message = similarity_ai(message)
            print(new_message)
            if len(new_message) < 4:
                new_message = message
                response = ask_openai(new_message)
            else:
                response = email_reuests(new_message)
            
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {})

