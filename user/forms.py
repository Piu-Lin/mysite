from django import forms
from django.contrib import auth 
from django.contrib.auth.models import User
class LoginForm(forms.Form):
    username=forms.CharField(label='用户名',
                            widget=forms.TextInput(
                                        attrs={'class':'form-control','placeholder':'请输入用户名'}))
    password=forms.CharField(label='密码',
                            widget=forms.PasswordInput(
                                        attrs={'class':'form-control','placeholder':'请输入密码'}))
    def clean(self):
        username= self.cleaned_data['username']
        password= self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:    
            raise forms.ValidationError('用户名密码错误')
        else:
            self.cleaned_data['user']=user
        return self.cleaned_data

class RegForm(forms.Form):
    username=forms.CharField(label='用户名',
                            max_length=20,
                            min_length=3,
                            widget=forms.TextInput(
                                        attrs={'class':'form-control','placeholder':'请输入3-20用户名'}))
    password=forms.CharField(label='密码',
                            min_length=6,
                            max_length=30, 
                            widget=forms.PasswordInput(
                                        attrs={'class':'form-control','placeholder':'请输入密码'}))

    passwordAgain=forms.CharField(label='请再输入一次密码',
                        min_length=6,
                        max_length=30,  
                        widget=forms.PasswordInput(
                                    attrs={'class':'form-control','placeholder':'请再输入一次密码'}))
   
    email=forms.EmailField(label='邮箱',
                            widget=forms.EmailInput(
                                            attrs={'class':'form-control','placeholder':'请输入邮箱'}))
                    
    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已注册')
        return email

    def clean_passwordAgain(self):
        password=self.cleaned_data['password']
        print(self.cleaned_data)
        passwordAgain=self.cleaned_data['passwordAgain']
        if passwordAgain != password:
            raise forms.ValidationError('密码不一致')
        return password

class ChangeNicknameFrom(forms.Form):
    newNickname=forms.CharField(
                            label='新的昵称',
                            max_length=20,
                            widget=forms.TextInput(
                            attrs={'class':'form-control','placeholder':'请输入新的昵称'})
    )
    def __init__(self,*args, **kwargs):
        if 'user' in kwargs:
            self.user=kwargs.pop('user')
        super(ChangeNicknameFrom,self).__init__(*args,**kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user']=self.user
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入旧的密码'}
        )
    )
    new_password = forms.CharField(
        label='新的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入新的密码'}
        )
    )
    new_password_again = forms.CharField(
        label='请再次输入新的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请再次输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证新的密码是否一致
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        # 验证旧的密码是否正确
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码错误')
        return old_password


class BindEmailForm(forms.Form):
    '''
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class':'form-control', 'placeholder':'请输入正确的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}
        )
    )
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)
    '''
    pass