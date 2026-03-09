from math import remainder
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from shared.models import BaseModel
from datetime import datetime,timedelta
from config.settings import EMAIL_EXPIRATION_TIME,PHONE_EXPIATION_TIME
import uuid
import random,string
from rest_framework_simplejwt.tokens import RefreshToken


ORDINARY_USER, ADMIN, MANAGER, = ('ordinary_user', 'admin', 'manager')
NEW, CODE_VERIFY, DONE, PHOTO_DONE, = ('new', 'code_verify',  'done', 'photo_done')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')





class CustomUser(AbstractUser,BaseModel):
    USER_ROLE =(
        (ORDINARY_USER,ORDINARY_USER),
        (ADMIN,ADMIN),
        (MANAGER,MANAGER)

    )
    USER_AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFY, CODE_VERIFY),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE)

    )
    USER_AUTH_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)

    )
    user_role = models.CharField(max_length=30, choices=USER_ROLE, default=ORDINARY_USER)
    auth_status = models.CharField(max_length=30, choices=USER_AUTH_STATUS, default=NEW)
    auth_type = models.CharField(max_length=30 ,choices=USER_AUTH_TYPE)
    email=models.EmailField(max_length=50,blank=True, null=True, unique=True)
    phone_number =  models.CharField(max_length=13, blank=True, null=True , unique=True)
    photo = models.ImageField(
        upload_to='user_photos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    def __str__(self):
        return self.username


    def check_username(self):
        if not self.username:
            temp_username = f'username{uuid.uuid4().__str__().split('-')[-1]}'
            while CustomUser.objects.filter(username=temp_username).exists():
                temp_username = f'{username}{uuid.uuid4().__str__().split("-")[-1]}'
            self.username = temp_username


    def check_pass(self):
        if not self.password:
            self.password = f'username{uuid.uuid4().__str__().split("-")[-1]}'

    def hashing_pass(self):
        if  not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def check_email(self):
        if self.email:
            email_normalize=self.email.lower()
            self.email=email_normalize


    def clean(self):
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hashing_pass()


    def token(self):
        refresh_token =RefreshToken.for_user(self)
        data = {
            'refresh':str(refresh_token),
            'access': str(refresh_token.access_token)
        }
        return data

    def generate_code(self, verify_type):
        d = string.ascii_letters
        b = string.digits
        m = d + b
        code = ''
        for i in range(4):
            belgi = random.choice(m)
            code = code + belgi
        CodeVerify.objects.create(
            code=code,
            users=self,
            verify_type=verify_type,
        )
        return code




    def save(self,*args ,**kwargs):
        self.clean()
        super().save(*args ,**kwargs)






class CodeVerify(models.Model):
    VERIFY_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)

    )
    users = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='verify_codes')
    code = models.CharField(max_length=4)
    verify_type=models.CharField(max_length=30, choices=VERIFY_TYPE)
    expiration_time = models.DateTimeField()
    is_active= models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expiration_time = timezone.now() + timedelta(minutes=EMAIL_EXPIRATION_TIME)
        else:
            self.expiration_time = timezone.now() + timedelta(minutes=PHONE_EXPIATION_TIME)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.users.username} | {self.code}'









