import base64
import os.path
from email.mime.text import MIMEText

from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
from properties import TEXT_EMAIL

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.compose']
path = os.path.abspath('/home/dan/projects/simpleRelay')
path_token = os.path.join(path, 'token.json')
path_client = os.path.join(path, 'client_secrets.json')


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(path_token):
        creds = Credentials.from_authorized_user_file(path_token, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print('missing/invalid token')
            exit()
        with open(path_token, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    try:
        message = (service.users().messages().send(userId='me', body=create_message(None, None, None, None))
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def create_message(sender, to, subject, message_text):
    message = MIMEText('test')
    message['to'] = TEXT_EMAIL
    message['from'] = 'pi'
    message['subject'] = 'pi text'
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


if __name__ == '__main__':
    main()