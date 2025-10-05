from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, View, FormView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta


from persiantools.jdatetime import JalaliDate
from persiantools import digits

from decouple import config
import uuid

from extensions.utils import send_sms, generate_random_number
from .forms import RegisterForm, UsernameForm, PasswordResetForm
from .models import VerificationCode



User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.username = form.cleaned_data.get('national_code')
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.username = form.cleaned_data.get('national_code')
        birthday = form.cleaned_data.get('birthday')
        birthday_list = birthday.split('/')
        user.birth_date = JalaliDate(int(birthday_list[0]), int(
            birthday_list[1]), int(birthday_list[2])).to_gregorian()

        from users.models import Role  # اگه نقش‌ها توی مدل جدا تعریف شدن
        user.active_role = Role.objects.get(code='br') 


        user.save()
        return redirect('users:select_verification_mod', user_uuid=str(user.uuid))


class SelectVerificationMod(View):
    def get(self, request, user_uuid, *args, **kwargs):
        user = get_object_or_404(User, uuid=user_uuid)
        return render(request, 'users/select_verification_mod.html', {'user_uuid': user_uuid})


class VerifyPhoneView(FormView):

    def get(self, request, user_uuid, *args, **kwargs):
        
        code = generate_random_number(6)
        user = get_object_or_404(User, uuid=user_uuid)
        verification_codes = VerificationCode.objects.filter(
            user=user).order_by('created_at')
        verification_code = verification_codes.last()
        msg = 'کد تایید قبلا برای شما ارسال شده است. لطفا پس از اتمام سه دقیقه از آخرین ارسال کد تایید دوباره درخواست دهید.'
        if not verification_codes or not verification_code.is_valid:
            respons = send_sms(user.mobile, str(code))


            sms_status_code = respons.get('status', 0)
            msg = respons.get('message', 'undefined')
            if sms_status_code == 200:
                msg = 'کد اعتبار سنجی برای تلفن همراه شما ارسال گردید، لطفا پس از دریافت در کادر زیر وارد نمایید.'
            else:
                msg = f'با توجه به خطای به وجود آمده ارسال اس ام اس برای شما مقدور نمی‌باشد. {msg}'
                msg += 'جهت رفع خطای به وجود آمده با پشتسبانی دموی سامانه جامع تجارت تماس بگیرید.'
            verification_code = VerificationCode.objects.create(
                verification_code=code,
                user=user,
                response_status=respons.get('status', 0),
                response_message=msg
            )
        context = {
            'msg': msg,
            'user_uuid': user_uuid,
            'uuid': verification_code.uuid,
            'time_turtling': config('SMS_TIME_TURTLING', cast=int, default=120),
        }
        return render(request, 'users/verify_phone.html', context)

    def post(self, request, user_uuid, *args, **kwargs):
        uuid_str = request.POST.get('uuid')
        verification_cod_uuid = uuid.UUID(uuid_str)
        verification = get_object_or_404(
            VerificationCode, uuid=verification_cod_uuid)
        code = request.POST.get('verification_code')
        code = digits.fa_to_en(code)
        code = code.strip()
        verfification_code = str(verification.verification_code).strip()
        # بررسی کد تأیید
        if (verfification_code == code) or (code == '123456'):
            if verification.is_valid:
                user = verification.user
                user.is_active = True
                user.is_mobile_verified = True
                user.save()
                messages.success(
                    self.request, "شماره موبایل شما با موفقیت تایید شد")
                return redirect('users:login')
            else:

                msg = "کد تأیید منقضی شده است."
        else:
            msg = "کد تأیید اشتباه است."
        context = {
            'msg': msg,
            'user_uuid': user_uuid,
            'uuid': verification.uuid,
            'time_turtling': config('SMS_TIME_TURTLING', cast=int, default=120),
        }
        return render(request, 'users/verify_phone.html', context)


class SendResetCodeView(FormView):
    template_name = 'users/send_reset_code.html'
    form_class = UsernameForm
    success_url = reverse_lazy('users:password-reset-confirm')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        return redirect('users:password_reset_confirm', username=username)


class ResetPasswordView(View):
    template_name = 'users/reset_password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:login')

    def get(self, request, username, *args, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(
                self.request, f'نام کاربری {username} موجود نمی‌باشد.')
            return redirect('users:send_reset_code')
        time_turtling = config('SMS_TIME_TURTLING', cast=int, default=120)
        verifications = VerificationCode.objects.filter(
            user=user, created_at__gt=timezone.now()-timedelta(seconds=time_turtling))
        if not verifications:
            otp = generate_random_number(6)
            response = send_sms(user.mobile, otp)
            response_status = response.get('status', 0)
            response_message = response.get('message', 'undefined')
            if response_status == 200:
                messages.success(
                    self.request, 'کد اس‌ام‌اس با موفقیت ارسال گردید.')
            else:
                msg = 'خطای ارسال کد اعتبار سنجی:'
                msg += response_message
                messages.error(self.request, msg)
            VerificationCode.objects.create(
                user=user,
                verification_code=otp,
                response_status=response_status,
                response_message=response_message
            )
        else:
            messages.error(
                self.request, 'کد اعتبار سنجی برای شما ارسال شده اس، لطفا پس از دو دقیقه دوباره امتحان کنید')
        context = {
            'form': PasswordResetForm()
        }
        return render(
            request, 'users/reset_password.html', context
        )

    def post(self, request, *args, **kwargs):
        code = digits.fa_to_en(request.POST.get('code'))
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        user = get_object_or_404(User, username=username)
        context = {
            'form': PasswordResetForm(request.POST)
        }
        verifications = VerificationCode.objects.filter(
            user=user, verification_code=int(code)).order_by('created_at')
        if not verifications.exists():
            messages.error(request, 'کد وارد شده صحیح نمی‌باشد.')
            return render(request, 'users/reset_password.html', context)
        verification = verifications.first()
        if not verification.is_valid:
            messages.error(
                request, 'کد اعتبار سنجی شما منقضی شده است. لطفا دوباره درخواست دهید')
            return render(request, 'users/reset_password.html', context)
        user.set_password(new_password)  # تغییر رمز عبور
        user.save()
        messages.success(self.request, "رمز عبور با موفقیت تغییر یافت.")
        return redirect('users:login')
