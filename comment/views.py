from django.shortcuts import render,redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .forms import CommentForm
# Create your views here.
def updataComment(req):
    referer=req.META.get('HTTP_REFERER',reverse('home'))
    commentForm=CommentForm(req.POST,user=req.user) 
    if commentForm.is_valid():
        comment=Comment()
        comment.user=commentForm.cleaned_data['user']
        comment.text=commentForm.cleaned_data['text']
        comment.content_object=commentForm.cleaned_data['content_object']
        comment.save()
        return redirect(referer)
    else:
        return render(req,'error.html',{'message':commentForm.errors,'redirect':referer})