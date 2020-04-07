from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
class CommentForm(forms.Form):
    contentType=forms.CharField(widget=forms.HiddenInput)
    objectsID=forms.IntegerField(widget=forms.HiddenInput)
    text=forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),label=False)
    def __init__(self,*args, **kwargs):
        if 'user' in kwargs:
            self.user=kwargs.pop('user')
        super(CommentForm,self).__init__(*args,**kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user']=self.user
        else:
            raise forms.ValidationError('用户未登录')
        contentType=self.cleaned_data['contentType']
        objectsID=self.cleaned_data['objectsID']
        try:
            modelClass=ContentType.objects.get(model=contentType).model_class()
            modelObject=modelClass.objects.get(pk=objectsID)
            self.cleaned_data['content_object']=modelObject
        except ObjectDoesNotExist:
            raise forms.ValidationError("对象不存在")
        return self.cleaned_data