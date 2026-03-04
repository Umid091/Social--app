from django.http.request import validate_host
from rest_framework import serializers,status
from shared.utility import check_email_or_phone
from .models import CustomUser, CodeVerify, VIA_EMAIL,VIA_PHONE
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from shared.utility import send_email


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    auth_status =serializers.CharField(read_only=True)
    auth_type = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email_or_phone'] = serializers.CharField(write_only=True, required=True)




    class Meta:
        model =CustomUser
        fields=['id', 'auth_status', 'auth_type']


    def create(self, validate_data):
        user =super().create(validate_data)
        if user.auth_type==VIA_EMAIL:
            code=user.generate_code(VIA_EMAIL)
            send_email(user.email, code)
            print(code,'----------------------------------------------------------')

        elif user.auth_type ==VIA_PHONE:
            code=user.generate_code(VIA_PHONE)
            print(code,'========================++++++++++++++++++++++++++++++++==========')

        else:
            raise ValidationError("Email yoki telifon raqam xato")

        return user


    
    def validate(self, attrs):
        super().validate(attrs)
        data = self.auth_validate(attrs)
        return data

    @staticmethod
    def auth_validate(user_input):
        email_or_phone = user_input.get('email_or_phone')

        try:
            user_input_type = check_email_or_phone(email_or_phone)
        except ValueError:
            raise ValidationError({
                'message': 'Email yoki telefon raqam xato kiritilgan. Iltimos qaytadan kiriting!!'
            })

        if user_input_type == 'phone':
            data = {
                'auth_type': VIA_PHONE,
                'phone_number': email_or_phone
            }
        elif user_input_type == 'email':
            data = {
                'auth_type': VIA_EMAIL,
                'email': email_or_phone
            }
        else:
            raise ValidationError({'message': 'Email yoki telefon raqam xato'})

        return data


    def validate_email_or_phone(self, value):
        if CustomUser.objects.filter(
                Q(phone_number=value) | Q(email=value)
        ).exists():
            raise ValidationError('Bu email yoki telefon raqam oldin ro\'yxatdan o\'tgan')

        return value


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['message'] = 'Kodingiz yuborildi'
        data['refresh'] = instance.token()['refresh']
        data['access'] = instance.token()['access']

        return data





