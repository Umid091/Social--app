import re
from rest_framework import status
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


phone_regex = re.compile(r'^\+998[0-9]{9}$')
email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
username_regex = re.compile(r'^[a-zA-Z0-9_.-]{3,30}$')


def check_email_or_phone(user_input):
    if re.fullmatch(phone_regex, user_input):
        data ='phone'

    elif re.fullmatch(email_regex,user_input):
        data='email'
    else:
        response={
            'status': status.HTTP_400_BAD_REQUEST,
            'messages' :'Email yoki telifon raqamingiz xato kiritilgan iltimos qaytadan tekshirib kiriting',
        }
        raise ValueError(response)
    return data



def send_email(email, code):
    send_mail(
        subject='Tasdiqlash kodi',
        message=f'Sizning tasdiqlash kodingiz....: {code}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
    )



def check_email_or_phone_or_username(user_input):
    if re.fullmatch(phone_regex, user_input):
        data ='phone'

    elif re.fullmatch(email_regex,user_input):
        data='email'
    elif re.fullmatch(username_regex,user_input):
        return 'username'

    else:
        response={
            'status': status.HTTP_400_BAD_REQUEST,
            'messages' :'Email yoki telifon raqamingiz xato kiritilgan iltimos qaytadan tekshirib kiriting',
        }
        raise ValueError(response)
    return data

