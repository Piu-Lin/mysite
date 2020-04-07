from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    nickname=models.CharField(max_length=20,verbose_name="昵称")
    def __str__(self):
        return '<Profile: %s for %s>' %(self.nickname,self.user.username)

def getNickname(self):
    if Profile.objects.filter(user=self).exists():
        profile=Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''

def getNicknameOrUsername(self):
    if Profile.objects.filter(user=self).exists():
        profile=Profile.objects.get(user=self)
        return profile.nickname
    else:
        self.username

def haveNickname(self):
    return Profile.objects.filter(user=self).exists()

User.getNickname=getNickname
User.haveNickname=haveNickname
User.getNicknameOrUsername=getNicknameOrUsername