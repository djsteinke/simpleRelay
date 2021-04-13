import base64
import os.path
from email.mime.text import MIMEText

from googleapiclient import errors
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from properties import TEXT_EMAIL

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.compose']
path = os.path.abspath('/home/pi/projects/simpleRelay')
path_token = os.path.join(path, 'token.json')
path_client = os.path.join(path, 'client_secrets.json')


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


class Text(object):
    def __init__(self, message_text):
        self._credentials = None
        if os.path.exists(path_token):
            self._credentials = Credentials.from_authorized_user_file(path_token, SCOPES)
        if not self._credentials or not self._credentials.valid:
            if self._credentials and self._credentials.expired and self._credentials.refresh_token:
                self._credentials.refresh(Request())
            else:
                print('Missing/Invalid token. Follow steps to create token.')
                exit()
            with open(path_token, 'w') as token:
                token.write(self._credentials.to_json())
        self._msg = create_message('me', TEXT_EMAIL, 'RPi Garage', message_text)

    def send(self):
        service = build('gmail', 'v1', credentials=self._credentials)
        try:
            message = (service.users().messages().send(userId='me', body=self._msg)
                       .execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
