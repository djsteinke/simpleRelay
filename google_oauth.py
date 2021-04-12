from __future__ import print_function
import os.path
import threading
import time

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['email']
path = os.path.abspath('/home/pi/projects/simpleRelay')
path_token = os.path.join(path, 'token.json')
path_client = os.path.join(path, 'client_secrets.json')
secrets = {}
device = {}
creds = None


def main():
    global secrets, path_token, path_client, device, creds
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(path_client):
        par = json.loads(open(path_client, "r").read())
        secrets = par['installed']
    else:
        print('client_secrets.json missing')
        exit()

    if os.path.exists(path_token):
        token_str = open(path_token, 'r')
        creds = Credentials(token_str, scopes=SCOPES, client_id=secrets['client_id'], client_secret=secrets['client_secret'])
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            check_email()
        else:
            url = 'https://oauth2.googleapis.com/device/code'
            client_id = '769546523664-28ib024nreraldlosa7rsadtngedjabd.apps.googleusercontent.com'
            headers = {'Content-type': 'application/x-www-form-urlencoded'}
            data = f'client_id={client_id}&scope=email%20profile'
            r = requests.post(url=url, headers=headers, data=data)
            r_str = r.content
            r_json = json.loads(r_str)
            print(r_str)
            device = r_json
            check_auth()
    else:
        check_email()


def check_auth():
    global secrets, path_token, device, creds
    url = 'https://oauth2.googleapis.com/token'
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    data = f'client_id={secrets["client_id"]}&client_secret={secrets["client_secret"]}&device_code={device["device_code"]}'
    data += '&grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code'
    r = requests.post(url=url, headers=headers, data=data)
    r_str = r.content
    r_json = json.loads(r_str)
    print(json.dumps(r_json))
    if 'error' in r_json:
        time.sleep(device['interval'])
        check_auth()
    elif 'access_token' in r_json:
        creds = Credentials.from_authorized_user_file(path_client, SCOPES)
        creds.token = r_json
        f = open(path_token, "w")
        f.write(creds.to_json())
        check_email()
    else:
        print(json.dumps(r_json))


def check_email():
    global creds
    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


if __name__ == '__main__':
    main()

