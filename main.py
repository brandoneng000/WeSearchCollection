from time import sleep
from zipfile import ZipFile
from decouple import config
from random import shuffle

import requests

def main():
    NUMBER_OF_FILES = 20
    zip_file = '446c8aa0-6eba-11e5-bc7f-4851b79b387c.zip'
    auth = get_authenitcation()
    token = get_token(auth)
    collection_name = "interview"
    statuses = []

    create_collection(token, collection_name)

    with ZipFile(zip_file, 'r') as zip:
        files = zip.namelist()
        counter = 0
        for file in files:
            if counter == NUMBER_OF_FILES:
                responses = get_manifest(token, collection_name)
                print(responses)
                break
            data = zip.read(file)
            reference = add_document(token, collection_name, data)
            statuses.append(tuple((file, reference)))
            counter += 1

    # delete_collection(token, collection_name)

def check_status(token: str, collection_name: str, reference: str):
    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(f'https://project-apollo-api.stg.gc.casetext.com/v0/language-modern-political/tasks/{reference}', headers=headers)

    return response.json()

def get_manifest(token: str, collection_name: str):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(f'https://project-apollo-api.stg.gc.casetext.com/v0/{collection_name}', headers=headers)
    
    return response.json()['documents']

def add_document(token: str, collection_name: str, data: str) -> str:
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'text/plain',
    }

    response = requests.post(f'https://project-apollo-api.stg.gc.casetext.com/v0/{collection_name}', headers=headers, data=data)

    return response.json()['reference']


def delete_collection(token: str, collection_name: str):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.delete(f'https://project-apollo-api.stg.gc.casetext.com/v0/{collection_name}/delete', headers=headers)
    print(response)

def create_collection(token: str, collection_name: str):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    data = '{ "model": "lawbert" }'

    response = requests.post(f'https://project-apollo-api.stg.gc.casetext.com/v0/{collection_name}/create', headers=headers, data=data)

    print(response)

def get_token(auth: str) -> str:
    auth = auth.split(":")
    token = auth[1].replace('}', '').replace('"', '')

    return token

def get_authenitcation() -> str:
    email = config('EMAIL')
    password = config('PASS')
    headers = {
        'Content-Type': 'application/json',
    }

    data = f'{{"email":"{email}" ,"password":"{password}"}}'
    
    response = requests.post('https://project-apollo-api.stg.gc.casetext.com/v0/auth/login', headers=headers, data=data)
    
    return response.text

if __name__ == '__main__':
    main()