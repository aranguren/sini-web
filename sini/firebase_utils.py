from firebase_admin import messaging
from firebase_admin.messaging import Message
import firebase_admin
from firebase_admin import credentials
import datetime


def send_push_notification(device_token, title, body, image_url, data):
    message = messaging.Message(
            data,
            android=messaging.AndroidConfig(
                    ttl=datetime.timedelta(seconds=3600),
                    priority='normal',
                    notification=messaging.AndroidNotification(
                    title=title,
                    body=body,
                    icon='stock_ticker_update',
                    color='#f45342',
                    image= image_url, #'https://firebasestorage.googleapis.com/v0/b/sini-1529613608740.appspot.com/o/FCMImages%2Fphoto1685036012.jpeg?alt=media&token=4b32205b-5e05-482c-bd08-eaa587146cf9',
                    ),

            ),
            token=device_token
    )
    response = messaging.send(message)
    return response

def send_push_notification_multi(device_tokens, title, body, data=None):
    #cred = credentials.Certificate(server_key)
    #firebase_admin.initialize_app(cred)

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        tokens=device_tokens
    )
    if data:
        message.data = data

    response = messaging.send_multicast(message)

    print("Successfully sent notification:", response)

    return response

    