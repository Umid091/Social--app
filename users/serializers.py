from rest_framework import serializers,status
from shared.utility import check_email_or_phone
from .models import CustomUser, CodeVerify, VIA_EMAIL,VIA_PHONE
from rest_framework.exceptions import ValidationError

class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    auth_status =serializers.CharField(read_only=True,required=True)
    auth_type = serializers.CharField(read_only=True, required=True)

    def __init__(self):
        super().__init__()
        super.fields['email_or_phone'] = serializers.CharField(write_only=True,required=True)





    class Meta:
        model =CustomUser
        fields=['id', 'auth_status', 'verify_type']


    @staticmethod
    def auth_validate(user_input):
        user_input_type =check_email_or_phone(user_input)
        if user_input_type=='phone':
            data ={
                'auth_type' :VIA_PHONE,
                'phone_number': user_input
            }

        elif user_input_type =='email':
            data = {
                'auth_type': VIA_EMAIL,
                'eamil': user_input
            }
        else:
            response = {
                'status': status.HTTP_400_BAD_REQUEST,
                'messages': 'Email yoki telifon raqamingiz xato kiritilgan iltimos qaytadan tekshirib kiriting',
            }
            raise ValueError(response)

        return data



