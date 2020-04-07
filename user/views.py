from django.shortcuts import render ,redirect
from django.http import JsonResponse
# Create your views here.
import string
import random
import time
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm,RegForm,ChangeNicknameFrom,BindEmailForm,ChangePasswordForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail

def login(req):
    if req.method == 'POST':
        loginForm=LoginForm(req.POST)
        if loginForm.is_valid():
            user=loginForm.cleaned_data['user']
            auth.login(req, user)
            return redirect(req.GET.get('from',reverse('home')))
    else:
        loginForm=LoginForm()
    context={}
    context['loginForm']=loginForm
    return render(req,'login.html',context)

def register(req):
    if req.method == 'POST':
        regForm=RegForm(req.POST)   
        if regForm.is_valid():
            username=regForm.cleaned_data['username']
            password=regForm.cleaned_data['password']
            email=regForm.cleaned_data['email']
            user=User.objects.create_user(username,email,password)
            user.save()
            user=auth.authenticate(username=username,password=password)
            auth.login(req, user)
            return redirect(req.GET.get('from',reverse('home')))
    else:
        regForm=RegForm()
    context={}
    context['regForm']=regForm
    return render(req,'register.html',context)

def logout(req):
    auth.logout(req)
    return redirect(req.GET.get('from',reverse('home')))

def userInfo(req):
    context={}
    return render(req,'userInfo.html',context)

def changeNickname(req):
    if req.method=="POST":
        form=ChangeNicknameFrom(req.POST,user=req.user)
        if form.is_valid():
            newNickname=form.cleaned_data['newNickname']
            profile,created=Profile.objects.get_or_create(user=req.user)
            profile.nickname=newNickname
            profile.save()
            return redirect(req.GET.get('from',reverse('home')))
    else:
        form=ChangeNicknameFrom()
    context={}
    context['form']=form
    context['pageTitle']='修改昵称'
    context['formTitle']='修改昵称'
    context['submitText']='修改'
    context['returnBackUrl']= req.GET.get('from',reverse('home'))
    return render(req,'form.html',context)

def bindEmail(request):
    pass
    '''
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            pass
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['pageTitle'] = '绑定邮箱'
    context['formTitle'] = '绑定邮箱'
    context['submitText'] = '绑定'
    context['form'] = form
    context['returnBackUrl'] = redirect_to
    return render(request, 'bind_email.html', context)
    '''

def send_verification_code(request):
    pass
    '''
    email = request.GET.get('email', '')
    data = {}

    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now
            
            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码：%s' % code,
                '1539636195@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
    '''

def change_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()
    context = {}
    context['pageTitle'] = '修改密码'
    context['formTitle'] = '修改密码'
    context['submitText'] = '修改'
    context['form'] = form
    context['returnBackUrl'] = redirect_to
    return render(request, 'form.html', context)