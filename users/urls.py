from django.urls import path

from config.urls import path
from .views import SignUpView, CodeVerifyView, GetNewCode,UserChangeView

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('code_verify/', CodeVerifyView.as_view()),
    path('get-new-code/', GetNewCode.as_view()),
    path('user-update/', UserChangeView.as_view()),
]