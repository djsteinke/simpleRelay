from __future__ import print_function
import os.path
import threading

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


def main():
    global secrets, path_token, path_client
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(path_client):
        par = json.loads(open(path_client, "r").read())
        secrets = par['installed']
    else:
        print('client_secrets.json missing')
        exit()

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(path_token, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            url = 'https://oauth2.googleapis.com/device/code'
            client_id = '769546523664-28ib024nreraldlosa7rsadtngedjabd.apps.googleusercontent.com'
            headers = {'Content-type': 'application/x-www-form-urlencoded'}
            data = f'client_id={client_id}&scope=email%20profile'
            r = requests.post(url=url, headers=headers, data=data)
            r_str = r.content
            r_json = json.loads(r_str)
            print(r_str)
            check_auth(r_json)
        # Save the credentials for the next run
        with open(path_token, 'w') as token:
            token.write(creds.to_json())

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


def check_auth(device):
    global secrets, path_token
    url = 'https://oauth2.googleapis.com/token'
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    data = f'client_id={secrets["client_id"]}&client_secret={secrets["client_secret"]}&device_code={device["device_code"]}'
    data += '&grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code'
    r = requests.post(url=url, headers=headers, data=data)
    r_str = r.content
    print(r_str)
    r_json = json.loads(r_str)
    if "error" in r_json:
        threading.Timer(device['interval'], check_auth)
    elif "access_token" in r_json:
        f = open(path_token, "w")
        f.write(json.dumps(r_json, indent=4))
        main()
    else:
        print(r)
        exit()


if __name__ == '__main__':
    main()

