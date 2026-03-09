from django.http.request import validate_host
from rest_framework import serializers,status
from shared.utility import check_email_or_phone
from .models import CustomUser, CodeVerify, VIA_EMAIL,VIA_PHONE,CODE_VERIFY, DONE
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

        user.save()
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



from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser, CODE_VERIFY, DONE
import re


class UserChangeSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Parol kamida 8 ta belgidan iborat bo'lishi kerak!")
        if ' ' in value:
            raise ValidationError("Parolda bo'sh joy bo'lmasligi kerak!")
        return value

    def validate_username(self, value):
        value = value.strip()
        if len(value) < 3:
            raise ValidationError("Username kamida 3 ta belgi bo'lishi kerak!")
        if ' ' in value:
            raise ValidationError("Username da bo'sh joy bo'lmasligi kerak!")
        if not re.match(r'^[a-zA-Z0-9_.-]+$', value):
            raise ValidationError("Username faqat harf, raqam, '_', '-', '.' bo'lishi kerak!")
        if CustomUser.objects.filter(username=value).exists():
            raise ValidationError("Bu username band!")
        return value

    def validate_first_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise ValidationError("ism kamida 2 ta belgi bo'lishi kerak")
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s-]+$', value):
            raise ValidationError("ismda faqat harflar bo'lishi kerak")
        return value.title()

    def validate_last_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise ValidationError("Familiya kamida 2 ta belgi bo'lishi kerak")
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s-]+$', value):
            raise ValidationError("Familiyada faqat harflar bo'lishi kerak!")
        return value.title()

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationError({
                "confirm_password": "Parollar mos kelmadi"
            })
        return attrs

    def update(self, instance, validated_data):
        if instance.auth_status != CODE_VERIFY:
            raise ValidationError({"message": "Siz hali tasdiqlamagansiz"})
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        instance.set_password(validated_data.get('password'))
        instance.auth_status = DONE
        instance.save()
        return instance

















