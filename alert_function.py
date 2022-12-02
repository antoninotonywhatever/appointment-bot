import os
from twilio.rest import Client

def lambda_handler(event, context):
    # You get both of these from Twilio on account set up
    account_sid = os.environ['sid']
    auth_token = os.environ['auth']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
     body='The SMS message you want to send yourself when a change is detected',
     from_='The phone number Twilio gives you',
     to='Your phone number with country code in front of it. Eg, +15555555555'
    )
