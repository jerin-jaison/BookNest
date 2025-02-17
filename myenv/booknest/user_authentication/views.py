from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import time, random
from django.core.mail import send_mail


# Create your views here.
@never_cache
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username exists')
            return redirect('signup_page')
        
        if User.objects.filter(email = email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup_page')
        

        if password != confirmPassword:
            messages.error(request, 'Please enter the same password')
            return redirect('signup_page')
        
        
        user = User.objects.create_user(username = username, first_name = first_name, last_name = last_name , email = email , password=password) 
        user.save()
        messages.success(request, 'Signup successful!')

        otp = str(random.randint(100000, 999999))
        print(otp)

        # Store in session
        request.session['reset_otp'] = otp
        request.session['reset_email'] = email
        
        # Send email
        subject = 'Your OTP for SignUp '
        message = f'Your OTP is: {otp}'
        from_email = 'booknestt@gmail.com'
        send_mail  (subject, message, from_email, [email])
        
        messages.success(request, 'OTP sent successfully')
        return redirect('otp_page_login')

    return render(request, 'signup_page.html')



def otpLogin_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        # Verify OTP
        if entered_otp == request.session.get('reset_otp'):
            request.session['otp_validated'] = True
            messages.success(request, 'OTP verification successfull')
            return redirect('login_page')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            
    return render(request, 'otp_signup.html')

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Invalid credentials')  
            return render(request, 'login_page.html')


    return render(request, 'login_page.html')

@never_cache
@login_required(login_url='login_page')
def home_view(request):
    # if not request.user.is_authenticated or not request.session.get('is_authenticated'):  
    #     return redirect('login_page')
    return render(request, 'index.html')

@never_cache
def signout_view(request):
    request.session.flush()
    logout(request)
    return redirect('login_page')

def forgetPassword_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not User.objects.filter(email= email).exists():
            messages.error(request, 'Email not recognized')
            return redirect('forgetPassword_page')

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        print(otp)

        # Store in session
        request.session['reset_otp'] = otp
        request.session['reset_email'] = email
        
        # Send email
        subject = 'Your OTP for Password Reset'
        message = f'Your OTP is: {otp}'
        from_email = 'booknestt@gmail.com'
        send_mail  (subject, message, from_email, [email])
        
        messages.success(request, 'OTP sent successfully')
        return redirect('otp_page')
        
    return render(request, 'forget_password.html')

def otpSignup_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        # Verify OTP
        if entered_otp == request.session.get('reset_otp'):
            request.session['otp_validated'] = True
            messages.success(request, 'OTP verification successfull')
            return redirect('reEnterPassword_page')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            
    return render(request, 'otp_signup.html')


def reEnterPassword_view(request):
    if not request.session.get('reset_email'):
        messages.error(request, 'Please start the password reset process from the beginning.')
        return redirect('forget_password')

    if not request.session.get('otp_validated'):
        messages.error(request, 'Please verify your OTP first.')
        return redirect('forget_password')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
    
    

        if password == confirm_password:
            user = User.objects.get(email = request.session['reset_email'])
            user.set_password(password)
            user.save()

            # Clear session data
            request.session.pop('reset_otp', None)
            request.session.pop('reset_email', None)
            request.session.pop('otp_validated', None)
                
            messages.success(request, 'Password reset successful! Please login with your new password.')
            return redirect('login_page')
        
        else:
            messages.error(request, 'Enter the same password twice!!')
            return redirect('reEnterPassword_page')
    
    return render(request, 're-enter_password.html')