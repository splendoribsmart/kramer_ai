import requests
import json

def status_check(email):
    myQuestions = ['Is the cremation of my loved one complete?', 'What is the status of the death certificates?', 'When will the cremation be complete?', 'Can I order more death certificates?', 'Can I change the urn that I ordered?', 'Can I schedule an appointment to pick up?']


    monday_apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI4NTkyMDU2MCwiYWFpIjoxMSwidWlkIjo0NzUzNDUxMiwiaWFkIjoiMjAyMy0xMC0wM1QwMzo1NTo0Ny4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTQ4NDkxMSwicmduIjoidXNlMSJ9.OwcBr2zXF-PUTj7c_KtTBUdSNeB_rbOKJpGobiscFdI"
    monday_apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization" : monday_apiKey}

    # query = '{ boards (limit:5) {name id} }'
    query = """{
    items_by_column_values (board_id: 87610960, column_id: "email", column_value: {email}) {
    id
    name
    column_values { 
        title
        id
        type
        text
        value
    }
    }
    }
    """

    data = {'query' : query}

    r = requests.post(url=monday_apiUrl, json=data, headers=headers) # make request

    b = r.json()

    death_certificate = b['data']['items_by_column_values'][0]['column_values'][8]['text']

    print(death_certificate)

    # cleaned = json.dumps(b, indent=4)

    if choice_question[0:10] is myQuestions[0][0:10]:
        pass
    elif choice_question[0:10] is myQuestions[1][0:10]:
        pass
    elif choice_question[0:10] is myQuestions[2][0:10]:
        pass
    elif choice_question[0:10] is myQuestions[3][0:10]:
        pass
    elif choice_question[0:10] is myQuestions[4][0:10]:
        print('Yes you can')
    elif choice_question[0:10] is myQuestions[5][0:10]:
        pass