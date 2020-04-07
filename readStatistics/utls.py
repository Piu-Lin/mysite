import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,ReadDetail
from django.db.models import Sum
from django.utils import timezone
def readOnce(req,obj): 
    ct=ContentType.objects.get_for_model(obj)
    key="%s_%s_read" %(ct.model,obj.pk)
    if not req.COOKIES.get(key):
        #总读数数+1
        readnum , created =ReadNum.objects.get_or_create(content_type = ct, object_id=obj.pk)
        readnum.readNum+=1
        readnum.save()
        #当天阅读+1
        date=timezone.now().date()
        readDetail, created =ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        readDetail.readNum+=1
        readDetail.save()
    return key

def getWeekReadData(content_type):
    today=timezone.now().date()
    dates=[]
    readNums=[]
    for i in range(6,-1,-1):
        date=today-datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        readDetails=ReadDetail.objects.filter(content_type=content_type,date=date)
        result=readDetails.aggregate(readNumSum=Sum('readNum'))
        readNums.append(result['readNumSum'] or 0)
    return dates,readNums

def getTodayHotData(content_type):
    today=timezone.now().date()
    readDetails=ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-readNum')
    return readDetails[:7]

def getYesterdayHotData(content_type):
    today=timezone.now().date()
    yesterday=today-datetime.timedelta(days=1)
    readDetails=ReadDetail.objects.filter(content_type=content_type,date=yesterday).order_by('-readNum')
    return readDetails[:7]
'''
def getWeekHotData(content_type):
    today=timezone.now().date()
    date=today-datetime.timedelta(days=7)
    readDetails=ReadDetail.objects\
        .filter(content_type=content_type,date__lt=today,date__gte=date)\
        .values('content_type','object_id')\
        .annotate(readNumSum=Sum('readNum'))\
        .order_by('-readNumSum')
    return readDetails[:7]
'''
def getWeekHotData(content_type):
    pass
