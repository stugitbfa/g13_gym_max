from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import random

from django.shortcuts import render


# Temporary OTP store (use DB or session in real app)
otp_storage = {}

def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp

        # Send OTP
        send_mail(
            'Your OTP for GYM-MAX Email Verification',
            f'Hello, your OTP is: {otp}',
            'your_email@example.com',  # Replace with your email
            [email],
            fail_silently=False,
        )

        request.session['pending_email'] = email
        request.session['temp_user'] = {'username': username, 'password': password}

        messages.info(request, "OTP sent to your email.")
        return redirect('confirm_email')

    return render(request, 'web/register.html')


def email_confirmation(request):
    return render(request, 'web/email_confirmation.html')


def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get('otp')
        email = request.session.get('pending_email')

        if email in otp_storage and otp_storage[email] == user_otp:
            del otp_storage[email]  # Remove OTP once used
            user_data = request.session.pop('temp_user', {})

            # Simulate user creation (replace with actual DB model)
            print(f"User created: {user_data}")  # Debug

            messages.success(request, "Email verified successfully!")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP.")
            return redirect('verify_otp')

    return render(request, 'web/verify_otp.html')


def enter_email(request):
   if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        request.session['pending_email'] = email
        request.session['temp_user'] = {'username': username, 'password': password}

        otp = random.randint(100000, 999999)
        otp_storage[email] = otp

        send_mail(
            'GYM-MAX Email Verification',
            f'Your OTP is: {otp}',
            'your_email@example.com',  # Replace with your actual email
            [email],
            fail_silently=False,
        )

        messages.info(request, "OTP sent to your email.")
        return redirect('confirm_email')  # or 'verify_otp'

    
otp_storage = {}  # Temporarily store OTPs

def enter_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Save email to session
        request.session['pending_email'] = email

        # Generate and store OTP
        otp = random.randint(100000, 999999)
        otp_storage[email] = otp

        # Send OTP
        send_mail(
            'GYM-MAX Email Verification',
            f'Your OTP is: {otp}',
            'your_email@example.com',  # Replace with your email
            [email],
            fail_silently=False,
        )

        messages.info(request, "OTP sent to your email.")
        return redirect('verify_otp')

    return render(request, 'web/enter_email.html')