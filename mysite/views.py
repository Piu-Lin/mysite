from django.shortcuts import render ,redirect
# Create your views here.
from readStatistics.utls import getWeekReadData ,getTodayHotData,getYesterdayHotData
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.urls import reverse

def home(req):
    blogContentType=ContentType.objects.get_for_model(Blog)
    dates,readNums=getWeekReadData(blogContentType)
    context={}
    context['dates']=dates
    context['readNums']=readNums
    context['todayHot']=getTodayHotData(blogContentType)
    context['yesterHot']=getYesterdayHotData(blogContentType)
    return render(req,"home.html",context)
