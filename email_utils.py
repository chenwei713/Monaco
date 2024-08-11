import os.path
import base64
from email.mime.text import MIMEText

from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
          "https://www.googleapis.com/auth/gmail.addons.current.action.compose",
          "https://www.googleapis.com/auth/gmail.metadata",
          "https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.compose"]

recipients = ["chenweix7@gmail.com",
              "cx608@nyu.edu",
              "man_luo@foxmail.com"
              ]

class GmailClient:

    def __init__(self):
        """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        self.service = build("gmail", "v1", credentials=creds)

    def send_email(self, message_content):
        try:
            # Call the Gmail API
            # message = EmailMessage()
            message = MIMEText(message_content, 'html')

            # message.set_content(message_content)

            message["To"] = ",".join(recipients)
            message["From"] = "cxdev7@gmail.dev"
            message["Subject"] = "BLVD Apartment Alert"

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
            # pylint: disable=E1101
            send_message = (
              self.service.users()
              .messages()
              .send(userId="me", body=create_message)
              .execute()
            )


        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")


if __name__ == "__main__":
  gmailClient = GmailClient()
  gmailClient.send_email("")
