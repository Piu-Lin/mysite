from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from .models import Blog,blogType
from django.conf import settings
from django.db.models import Count
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from readStatistics.utls import readOnce
from comment.forms import CommentForm
# Create your views here.
    
def getBlogListCommonData(blogsAllList, reques):
    paginator=Paginator(blogsAllList,settings.EACH_PAGE_BLOGS_NUMBER) 
    pageNum=reques.GET.get('page',1) 
    pageOfBlogs=paginator.get_page(pageNum)
    currentPageNum=pageOfBlogs.number
    #pageRange=[currentPageNum-2,currentPageNum-1,currentPageNum,currentPageNum+1,currentPageNum+2]
    pageRange =[x for x in range(int(pageNum)-2, int(pageNum)+3) if 0 < x <= paginator.num_pages]
    if pageRange[0]-1>=2:
        pageRange.insert(0,"...")
    if paginator.num_pages-pageRange[-1]>=2:
        pageRange.append("...")
    if pageRange[0]!=1:
        pageRange.insert(0,1)
    if pageRange[-1]!=paginator.num_pages:
        pageRange.append(paginator.num_pages)

    context={}
    context['blogs']= pageOfBlogs.object_list
    context['pageOfBlogs'] = pageOfBlogs
    context['blogTypes'] =blogType.objects.annotate(blogCount= Count('blog'))
    context['pageRange'] =pageRange
    context['blogDates'] =Blog.objects.dates('createdTime','month',order='DESC')
    return context

def blogList(reques):
    blogsAllList=Blog.objects.all()
    context=getBlogListCommonData(blogsAllList,reques)
    return render(reques,"blogList.html",context)

def blogWithType(req,blogTypePk):
    blogtype= get_object_or_404(blogType,pk=blogTypePk)
    blogsAllList=Blog.objects.filter(blogType = blogtype)
    context=getBlogListCommonData(blogsAllList,req)
    context['blogtype']=blogtype
    return render(req,'blogWithType.html', context) 

def blogWithDate(req,year,month):
    blogsAllList=Blog.objects.filter(createdTime__year = year,createdTime__month = month)
    context=getBlogListCommonData(blogsAllList,req)
    context['blogWithDate']= '%s年%s月' %(year,month)
    return render(req,'blogWithDate.html', context)

def blogDetail(req,blogPk):
    blog=get_object_or_404(Blog, pk=blogPk)
    readCookieKey=readOnce(req,blog)
    blogContentType=ContentType.objects.get_for_model(blog)
    comments=Comment.objects.filter(content_type=blogContentType,object_id=blog.pk)

    context={}
    
    context['previousBlog']=Blog.objects.filter(createdTime__gt=blog.createdTime).last()
    context['nextBlog']=Blog.objects.filter(createdTime__lt=blog.createdTime).first()
    context['blog']=blog
    context['comments']=comments
    data={}
    data['contentType']= blogContentType.model
    data['objectsID']= blogPk
    context['commentForm']=CommentForm(initial=data)
    response=render(req,'blogDetail.html',context)
    response.set_cookie(readCookieKey,True,max_age=120)
    return response