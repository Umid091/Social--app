import re
from http.client import responses

from pyexpat.errors import messages
from rest_framework import status
from rest_framework.response import Response



phone_regex = re.compile(r'^\+998[0-9]{9}$')
email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

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

