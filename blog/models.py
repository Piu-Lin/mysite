from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from readStatistics.models import ReadNumExpandMethod ,ReadDetail
# Create your models here.



class blogType(models.Model):
    typeName=models.CharField(max_length=15)
    def __str__(self):
        return self.typeName


class Blog(models.Model,ReadNumExpandMethod):
    title=models.CharField(max_length=50)
    blogType=models.ForeignKey(blogType, on_delete = models.DO_NOTHING)
    content=RichTextUploadingField()
    author= models.ForeignKey(User, on_delete = models.DO_NOTHING)
    createdTime=models.DateTimeField(auto_now_add=True)
    lastUpdateTime=models.DateTimeField(auto_now=True)
    isDeleted=models.BooleanField(default=False)
    readedNum=models.IntegerField(default=0) 
    readDetails=GenericRelation(ReadDetail)
    '''
    def getReadNum(self):
        try:
            return self.readnum.readNum
        except exceptions.ObjectDoesNotExist :
            return 0
    '''
    def __str__(self):
        return "<Blog: %s>" %self.title
    class Meta:
        ordering=["-createdTime"]
'''
class ReadNum(models.Model):
    readNum=models.IntegerField(default=0)
    blog=models.OneToOneField(Blog,on_delete=models.DO_NOTHING)
'''
