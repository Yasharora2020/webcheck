import boto3
import requests
import os
from dotenv import load_dotenv
load_dotenv()

ses_client = boto3.client('ses')


def handler(event, context):
    url = 'https://example.com/jwb' # replace with your website url
    response = requests.get(url)
    status_code = response.status_code
    
    
    if status_code != 200:
        subject = f'Website {url} is down!'
        body = f'The website {url} returned status code {status_code}. Please check it ASAP.'
        sender = os.environ.get('sender') # replace with your SES sender email address
        recipient = os.environ.get('recipient') # replace with the email address to receive the notification
        
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=sender
        )
        
        print(f'Email notification sent to {recipient} with response: {response}')
    else:
        print(f'Website {url} is up and running.')
    
    return {
        'statusCode': 200,
        'body': 'Website check complete'
    }

