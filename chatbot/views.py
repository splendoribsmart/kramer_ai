from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from . import trainer, monday
import re

from django.utils import timezone

import requests
import json


# GOLBAL FOR VARIABLES
openai_api_key = trainer.api_key() #"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"
openai.api_key = openai_api_key
choice_question = ''

# IA QUESTION SIMILARITY CHECKER
def similarity_ai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": '''you are a very very layperson, you are more human. you are cutomers srevice person and you are asked questions which you\'d check if the relate to or are simillar to any of the listed questions below but be sure to link highly identical questions together first. you respond with the exact question that the customers question is related or similar only the question nothing else attached, reply with just the qustion please remove numbering and if there are non related of similar you simpple respond with NO.
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
    global choice_question
    choice_question = answer
    return answer

# AI EMAIL REQUEST
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

# AI RESPONSE FORM MONDAY.COM
def monday_lookup(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You an asistance, you just werite what you've been given, no more that 40 words"},
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

def status_check(email):
    myQuestions = ['Is the cremation of my loved one complete?', 'What is the status of the death certificates?', 'When will the cremation be complete?', 'Can I order more death certificates?', 'Can I change the urn that I ordered?', 'Can I schedule an appointment to pick up?']


    monday_apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI4NTkyMDU2MCwiYWFpIjoxMSwidWlkIjo0NzUzNDUxMiwiaWFkIjoiMjAyMy0xMC0wM1QwMzo1NTo0Ny4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTQ4NDkxMSwicmduIjoidXNlMSJ9.OwcBr2zXF-PUTj7c_KtTBUdSNeB_rbOKJpGobiscFdI"
    monday_apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization" : monday_apiKey}

    # query = '{ boards (limit:5) {name id} }'
    # query = """{
    # items_by_column_values (board_id: 87610960, column_id: "email", column_value: {email}) {
    # id
    # name
    # column_values { 
    #     title
    #     id
    #     type
    #     text
    #     value
    # }
    # }
    # }
    # """

    query = f"""
    {{
        items_by_column_values (board_id: 87610960, column_id: "email", column_value: "{email}") {{
            id
            name
            column_values {{ 
                title
                id
                type
                text
                value
            }}
        }}
    }}
    """

    data = {'query' : query}

    r = requests.post(url=monday_apiUrl, json=data, headers=headers) # make request

    b = r.json()

    cremation_status = b['data']['items_by_column_values'][0]['column_values'][7]['text']
    death_certificate = b['data']['items_by_column_values'][0]['column_values'][8]['text']
    cremation_complete_time = b['data']['items_by_column_values'][0]['column_values'][36]['text']
    more_death_certificate = 'Additional death certificates can be ordered online by clicking on this link: https://ovra.txapps.texas.gov/ovra/order-death-certificate'
    check_email = b['data']['items_by_column_values'][0]['column_values'][5]['text']
    appointment = b['data']['items_by_column_values'][0]['column_values'][8]['text']

    # print(death_certificate)

    # cleaned = json.dumps(b, indent=4)

    print(choice_question in myQuestions)
    print(choice_question)
    print(choice_question == myQuestions[0])

    if choice_question in myQuestions:
        print(f'The question is:    {choice_question}')

        if choice_question[0:10] == myQuestions[0][0:10]:
            if cremation_status == '@Kramer':
                return 'Your loved one is in our care.'
            elif cremation_status == 'KC Return Approve':
                return 'Your loved one\'s urn is ready to be returned. Please schedule an appointment.'
            elif cremation_status == 'Kramer --> KC':
                return 'The cremation for your loved one will take place soon.'
            elif cremation_status == 'KC':
                return 'The cremation for your loved one is ongoing.'
            elif cremation_status == 'Urn To Mail':
                return 'We are preparing everything to mail.'
            elif cremation_status == 'URN RETURNED':
                return 'The urn has been returned.'
            else:
                return cremation_status

        elif choice_question[0:10] is myQuestions[1][0:10]:
            return death_certificate
        elif choice_question[0:10] is myQuestions[2][0:10]:
            return cremation_complete_time
        elif choice_question[0:10] is myQuestions[3][0:10]:
            return more_death_certificate
        elif choice_question[0:10] is myQuestions[4][0:10]:
            if check_email:
                return "Yes you can. When we notify you that everything is ready to be returned, please schedule an appointment. During your appointment you can make any changes you need in person."
            else:
                return "We couldn't locate your information in our database, so it appears you may not be an existing customer."
        elif choice_question[0:10] is myQuestions[5][0:10]:
            return appointment
    
    # comback
    else:
        return 'Can you bring clarity to the information you which to inquire?'
    #     message = requests.session['message']
    #     new_message = similarity_ai(message)
    #     print(new_message)
    #     if len(new_message) < 4:
    #         new_message = message
    #         response = ask_openai(new_message)
    #     else:
    #         response = email_reuests(new_message)
    #         global choice_question
    #         choice_question = new_message




# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        # requests.session['message'] = message

        # lst = re.findall('\S+@\S+', s)
        try:
            match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', message)
            email = match.group(0)
            print(match.group(0))
        except:
            email = "blank"

        if is_valid_email(email):
            print(f"{email} is a valid email address.")
            monday_feedback = status_check(email)
            # global my_content
            my_content = monday_feedback

            print("My content: ", my_content)
            print('Status Confirmed') #"Yes, we have your information in our database." #monday_lookup(email)
            response = monday_lookup(message=str(my_content))
        else:
            print(f"{email} is not a valid email address.")
            # response = "We couldn't locate your information in our database, so it appears you may not be an existing customer."

            if message[-1] == '?':
                new_message = similarity_ai(message) #my_content
                print("New Message: ", new_message)

                response = email_reuests(new_message)
                global choice_question
                choice_question = new_message

            # elif message[0:2] == 'NO' or message[0:2] == 'No' or message[0:2] == 'no':

            #     response = ask_openai(message)
            else:
                response = ask_openai(message)
                # response = email_reuests(new_message)
                # global choice_question
                # choice_question = new_message
                # requests.session['monday_question'] = new_message
            
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {})

