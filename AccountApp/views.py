from .utils import send_otp
from django.views import View
from .models import User, OTP
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from .forms import SignUpForm, SignInForm, EmailForm, CodeForm, ResetPasswordForm


class SignUpView(View):
    def get(self, request):
        return render(request, 'AccountApp/sign-up.html', {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'این ایمیل قبلاً ثبت شده است.')
                return redirect('AccountApp:sign-up')
            if len(password) < 8:
                messages.error(request, 'رمز عبور باید بیشتر از 8 کارکتر داشته باشد.')
            if password == confirm_password:
                user = User.objects.create_user(email=email, password=password)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('/')
            messages.error(request, 'رمز عبور و تایید رمز عبور یکسان نیستند.')
        if 'captcha' in form.errors:
            messages.error(request, 'لطفاً کپچا را به درستی حل کنید.')
        return render(request, 'AccountApp/sign-up.html', {'form': form})


class SignInView(View):
    def get(self, request):
        return render(request, 'AccountApp/sign-in.html', {'form': SignInForm()})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('/')
            messages.error(request, 'ایمیل یا رمز عبور اشتباه است')
            return redirect('AccountApp:sign-in')
        if 'captcha' in form.errors:
            messages.error(request, 'لطفاً کپچا را به درستی حل کنید.')
        return render(request, 'AccountApp/sign-in.html', {'form': form})


class ForgetPasswordView(View):
    def get(self, request):
        return render(request, 'AccountApp/forget-password.html', {'form': EmailForm()})

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                request.session['email'] = {'email': email}
                send_otp(email)
                messages.success(request, "کد تأیید ارسال شد.")
                return redirect('AccountApp:verify-code')
            messages.error(request, 'ایمیل وارد شده ثبت نشده است.')
            return redirect('AccountApp:forget-password')
        return render(request, 'AccountApp/forget-password.html', {'form': form})


class VerifyCodeView(View):
    def get(self, request):
        return render(request, 'AccountApp/verify-code.html', {'form': CodeForm()})

    def post(self, request):
        form = CodeForm(request.POST)
        if form.is_valid():
            email = request.session.get('email', {}).get('email')
            if not email:
                messages.error(request, "مشکلی در ارتباط با سرور به وجود آمد. لطفا مجدد تلاش کنید.")
                return redirect('AccountApp:forget-password')
            otp_instance = OTP.objects.get(email=email)
            if not otp_instance or otp_instance.is_expired():
                messages.error(request, "کد تایید منقضی شده یا نامعتبر است, لطفا مجدد تلاش کنید.")
                return redirect('AccountApp:verify-code')
            if form.cleaned_data['code'] == otp_instance.code:
                otp_instance.delete()
                return redirect('AccountApp:reset-password')
            form.add_error('code', 'کد معتبر نمیباشد.')
            return render(request, 'AccountApp/verify-code.html', {'form': form})


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'AccountApp/reset-password.html', {'form': ResetPasswordForm()})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = request.session.get('email', {}).get('email')
            user = User.objects.get(email=email)
            if not user:
                messages.error(request, "مشکلی در دریافت اطلاعات به وجود آمده. لطفا مجدد تلاش کنید.")
                return redirect('AccountApp:sign-up')
            password = form.cleaned_data.get('password')
            if len(password) >= 8:
                if password == form.cleaned_data.get('confirm_password'):
                    user.password = make_password(password)
                    user.save()
                    request.session.pop('email', None)
                    messages.success(request, 'رمز عبور با موفقیت عوض شد.')
                    return redirect('AccountApp:sign-up')
                messages.error(request, 'رمزها با یکدیگر مطابقت ندارند.')
            messages.error(request, 'رمز عبور باید بیشتر از 8 کارکتر داشته باشد.')
        return render(request, 'AccountApp/reset-password.html', {'form': form})
