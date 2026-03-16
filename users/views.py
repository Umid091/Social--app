from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import CustomUser, NEW, CodeVerify as CodeVerifyModel, DONE, PHOTO_DONE,VIA_PHONE,VIA_EMAIL,CODE_VERIFY
from shared.utility import send_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import token_blacklist
from rest_framework.generics import CreateAPIView
from .serializers import SignUpSerializer,UserChangeSerializer,PhotoStatusSerializer, LoginSeializer
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView

class SignUpView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer
    queryset = CustomUser.objects.all()


class CodeVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        code = request.data.get('code')

        codes = user.verify_codes.filter(
            code=code,
            expiration_time__gte=timezone.now(),
            is_active=True
        )

        if not codes.exists():
            raise ValidationError({
                "message": "kodingiz xato yoki eskirgan",
                'status': status.HTTP_400_BAD_REQUEST
            })

        codes.update(is_active=False)

        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFY
            user.save()

        tokens = user.token()
        response_data = {
            "message": "kod tasdiqlandi",
            "status": status.HTTP_200_OK,
            "access": tokens['access'],
            "refresh": tokens['refresh']
        }

        return Response(response_data)


class GetNewCode(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        user =request.user

        codes = user.verify_codes.filter(
            expiration_time__gte=timezone.now(),
            is_active=True
        )
        if codes.exists():
            raise ValidationError({ 'message': 'sizda hali activ kod bor'})

        else:
            if user.auth_type == VIA_EMAIL:
                code = user.generate_code(VIA_EMAIL)
                send_email(user.email, code)
                print(code, '----------------------------------------------------------')

            elif user.auth_type == VIA_PHONE:
                code = user.generate_code(VIA_PHONE)
                print(code, '========================++++++++++++++++++++++++++++++++==========')

        response_data = {
            "message": "kod yuborildi",
            "status": status.HTTP_201_CREATED,

        }
        return Response(response_data)


# views.py

class UserChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        if request.user.auth_status not in [CODE_VERIFY, DONE]:
            return Response({
                "message": "Siz hali kod tasdiqlamagansiz!"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = UserChangeSerializer(
            instance=request.user,
            data=request.data,
            partial=False
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "message": "Ma'lumotlar muvaffaqiyatli yangilandi",
            "username": user.username,
            "access": user.token()['access'],
            "refresh": user.token()['refresh']
        }, status=status.HTTP_200_OK)



class UserChangePhoto(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def patch(self, request):
        user =request.user
        serializer =PhotoStatusSerializer(data =request.data ,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user ,validated_data=serializer.validated_data)

        respons ={
            'message':"Rasm qo'shildi",
            'status':status.HTTP_200_OK,
            'access':user.token()['access'],
            "refresh": user.token()['refresh'],

        }
        return Response(respons)


# class LoginView(TokenObtainPairView):
#     serializer_class = LoginSeializer



class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSeializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        refresh = self.request.data.get('refresh')
        try:
            refresh_token = RefreshToken(refresh)
            refresh_token.blacklist()
        except Exception as a:
            raise ValidationError(detail='xatolik ')

        else:
            respons_data ={
                'status': status.HTTP_200_OK,
                'message':'tizimdan chiqdinggzi'
        }
            return Response(respons_data)

class LoginRefresh(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self,request):
        refresh =self.request.data.get('refresh',None)
        try:
            refresh_token = RefreshToken(refresh)
        except Exception as e:
            raise ValidationError(detail='xatolik')
        else:
            respons_data ={
                'status':status.HTTP_201_CREATED,
                'access':str(refresh_token.access_token)
            }
            return Response(respons_data)


from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer

class ForgotPasswordView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        tokens = user.token()

        return Response({
            'message': 'Tasdiqlash kodi yuborildi.',
            'access': tokens['access'],
            'refresh': tokens['refresh'],
        }, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        user = request.user

        if user.auth_status == CODE_VERIFY:
            return Response(
                {'message': 'Avval tasdiqlash kodini kiriting'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ResetPasswordSerializer( instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user, validated_data=serializer.validated_data)

        tokens = user.token()
        return Response({
            'message': 'Parol muvaffaqiyatli yangilandi.',
            'access': tokens['access'],
            'refresh': tokens['refresh'],
        })





















