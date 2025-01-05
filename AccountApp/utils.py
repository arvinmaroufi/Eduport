from random import randint
from AccountApp.models import OTP
from django.core.mail import send_mail


def send_otp(email):
    code = randint(10000, 99999)
    print(code)
    OTP.objects.filter(email=email).delete()
    OTP.objects.create(email=email, code=code)
    if '@' in email:
        send_mail(
            'Welcome to NoonPost Shop',
            f'Your OTP code is {code}',
            'AshkanGhodrati0@gmail.com',
            [email]
        )
    else:
        pass
