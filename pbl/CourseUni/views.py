from django.shortcuts import render,redirect
from django.conf import settings
from .models import courses,categories,teacher,mycourses
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import math, random 
import os
# Create your views here.
def home(request):
    cats = categories.objects.all()
    crs = courses.objects.all()
    dic={}
    for cr in crs:
        if cr.category in dic:
            dic[cr.category]+=1
        else:
            dic[cr.category]=1
    access=False
    if request.user.is_authenticated:
        if teacher.objects.filter(name=request.user.username).exists():
            access=True
    if request.method=="POST":
        course=request.POST['course']
        category=request.POST['category']
        z=courses.objects.filter(name=course)
        q=courses.objects.filter(category=category)
        if z.exists() and q.exists():
            return render(request,'index.html',{'cats':cats,'crs':crs,'dic':dic,'access':access,'z':z})
        elif z.exists():
            return render(request,'index.html',{'cats':cats,'crs':crs,'dic':dic,'access':access,'z':z})
        else:
            z=q
            return render(request,'index.html',{'cats':cats,'crs':crs,'dic':dic,'access':access,'z':z})
    else:
        return render(request,'index.html',{'cats':cats,'crs':crs,'dic':dic,'access':access})
def index(request):
    cats = categories.objects.all()
    crs = courses.objects.all()
    dic={}
    for cr in crs:
        if cr.category in dic:
            dic[cr.category]+=1
        else:
            dic[cr.category]=1
    access=False
    if request.user.is_authenticated:
        if teacher.objects.filter(name=request.user.username).exists():
            access=True
    if request.method=="POST":
        course=request.POST['course']
        category=request.POST['category']
        z=courses.objects.filter(name=course)
        q=courses.objects.filter(category=category)
        if z.exists() and q.exists():
            return render(request,'index.html',{'cats':cats,'crs':crs,'dic':dic,'access':access,'z':z})
        elif z.exists():
            return render(request,'index.html',{'cats':cats,'crs':crs,'dic':dic,'access':access,'z':z})
        else:
            z=q 
            return render(request,'index.html',{'cats':cats,'crs':crs,'dic':dic,'access':access,'z':z})
    else:
        return render(request,'index.html',{'cats':cats,'crs':crs,'dic':dic,'access':access})
def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['pass']
        try:
            user=auth.authenticate(username=username,password=password)
        except:
            messages.info(request,"Invalid Credentials")
        if user is not None:
            auth.login(request,user)
            return redirect('/index')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
    else:
        return render(request,'login.html')
    return render(request,'login.html')
def signup(request):
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['pass1']
        password2=request.POST['pass2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exist")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email already exist")
            else:
                user=User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password1)
                user.save()
                auth.login(request,user)
                digits = "0123456789"
                OTP = ""  
                for i in range(6) : 
                    OTP += digits[math.floor(random.random() * 10)]
                from_email=settings.EMAIL_HOST_USER
                to_email=request.user.email
                subject="One Time Password For confirmation of CourseUni."
                msg=OTP
                val=msg
                send_mail(subject,msg,from_email,[to_email])
                return render(request,'confirmation.html',{'msg':msg})
        else:
            messages.info(request,"Password not matching")
            return redirect('signup')
    else:
        return render(request,'signup.html')
def confirmation(request,val):
    if request.method=="POST":
        otp=request.POST['otp']
        if otp==val:
            from_email=settings.EMAIL_HOST_USER
            to_email=request.user.email
            subject="Welcome to CourseUni"
            msg="Find the best online courses here, and we hope you take knowledge most out of it !! Thank you!"
            send_mail(subject,msg,from_email,[to_email])
            return redirect('index')
        else:
            success="Wrong OTP"
            User.objects.filter(username=request.user.username).delete()
    return render(request,'confirmation.html',{'success':success})   

def course(request):
    crs = courses.objects.all()
    access=False
    if request.user.is_authenticated:
        if teacher.objects.filter(name=request.user.username).exists():
            access=True
    s=""
    if request.method=="POST":
        course=request.POST['course']
        category=request.POST['category']
        z=courses.objects.filter(name=course)
        q=courses.objects.filter(category=category)
        if z.exists() and q.exists():
            crs=z
            return render(request,'course.html',{'crs':crs,'access':access,'s':s})
        elif z.exists():
            crs=z
            return render(request,'course.html',{'crs':crs,'access':access,'s':s})
        else:
            crs=q 
            return render(request,'course.html',{'crs':crs,'access':access,'s':s})
    return render(request,'course.html',{'crs':crs,'access':access,'s':s})
def contact(request):
    access=False
    if request.user.is_authenticated:
        if teacher.objects.filter(name=request.user.username).exists():
            access=True
    success=""
    if request.method=="POST":
        from_email=request.user.email
        to_email=settings.EMAIL_HOST_USER
        subject=request.POST['subject']
        mess=request.POST['message_text']
        send_mail(subject,mess,from_email,[to_email])
        success="Mail sent successfully!"
    return render(request,'contact.html',{'access':access,'success':success})
def category(request,value):
    access=False
    if request.user.is_authenticated:
        if teacher.objects.filter(name=request.user.username).exists():
            access=True
    crs = courses.objects.filter(category=value)
    if request.method=="POST":
        course=request.POST['course']
        z=courses.objects.filter(name=course,category=value)
        if z.exists():
            crs=z
            return render(request,'category.html',{'crs':crs,'access':access,'value':value})
    return render(request,'category.html',{'crs':crs,'access':access,'value':value})
def logout(request):
    auth.logout(request)
    return redirect('/index')
def signup_teacher(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            t_name = request.POST['name']
            t_email = request.POST['email']
            t_number = request.POST['number']
            t_course = request.POST['course']
            t_category = request.POST['category']
            t_course_file =request.FILES['course_file']
            if teacher.objects.filter(name=t_name).exists():
                messages.info(request,"Username already exist")
                return redirect('signup_teacher')
            elif teacher.objects.filter(email=t_email).exists():
                messages.info(request,"Email has been taken")
                return redirect('signup_teacher')
            else:
                if User.objects.filter(username=t_name).exists():
                    table = teacher(name=t_name,email=t_email,number=t_number,course=t_course,course_file=t_course_file,category=t_category)
                    table.save()
                    messages.info(request,"You are successfully registered as a Teacher.")
                    return redirect('signup_teacher')
                else:
                    messages.info(request,"Please, login as a member first")
                    return redirect('signup_teacher')
            
        else:
            return render(request,'signup_teacher.html')
    else:
        return redirect('/signup')
def myteachings(request):
    files = teacher.objects.filter(name=request.user.username)
    access=False
    if request.user.is_authenticated:
        if teacher.objects.filter(name=request.user.username).exists():
            access=True
    update=""   
    if request.method=="POST":
        teacher.objects.filter(name=request.user.username).update(course_file=request.FILES['course_file'])
        filename=request.FILES['course_file']
        p = default_storage.save(str(filename), ContentFile(filename.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, p)
        update="We have recieved your file, we will verify it and let you know soon !"
    return render(request,'myteachings.html',{'files':files,'update':update,'access':access})

def add_to(request,para):
    if request.user.is_authenticated:
        crs = courses.objects.all()
        access=False
        if request.user.is_authenticated:
            if teacher.objects.filter(name=request.user.username).exists():
                access=True
        if request.method=="POST":
            s=""
            if mycourses.objects.filter(name=request.user.username,mycourse=para).exists():
                s="This course is already in your mycourses"
                return render(request,'course.html',{'crs':crs,'s':s,'access':access})
            c=mycourses(name=request.user.username,mycourse=para)
            c.save()
            return redirect('mycourse')
        return render(request,'course.html',{'crs':crs,'access':access})
    else:
        return redirect('/signup')

def mycourse(request):
    access=False
    if request.user.is_authenticated:
        if teacher.objects.filter(name=request.user.username).exists():
            access=True
    c=mycourses.objects.filter(name=request.user.username)
    l=[]
    for i in c:
        a=courses.objects.filter(name=i.mycourse)
        for z in a:
            l.append(z)
    return render(request,'mycourse.html',{'access':access,'l':l})


def remove(request,par):
    if request.method=="POST":
        access=False
        if request.user.is_authenticated:
            if teacher.objects.filter(name=request.user.username).exists():
                access=True
        mycourses.objects.get(name=request.user.username,mycourse=par).delete()
        return redirect('mycourse')
    return render(request,'/')

def forgot(request):
    if request.method=="POST":
        mail=request.POST['email']
        if User.objects.filter(email=mail).exists():
            digits = "0123456789"
            OTP = ""  
            for i in range(6) : 
                 OTP += digits[math.floor(random.random() * 10)]
            from_email=settings.EMAIL_HOST_USER
            to_email=mail
            subject="One Time Password For resetting password."
            msg=OTP
            send_mail(subject,msg,from_email,[to_email])
            return render(request,'otp.html',{'mail':mail,'msg':msg})
        else:
            messages.info(request,"Email is not registered.")
            return render(request,'forgot.html')
    return render(request,'forgot.html')

def otp(request,data,ml):
    if request.method=="POST":
        otp=request.POST['otp']
        if otp==data:
            return render(request,'changepassword.html',{'ml':ml})
    return render(request,'otp.html')

def changepassword(request,one):
    if request.method=="POST":
        password1=request.POST['pass1']
        password2=request.POST['pass2']
        if password1==password2:
            u=User.objects.get(email=one)
            u.set_password(password1)
            u.save()
            return redirect('/index')
        else:
            messages.info(request,"Wrong confirmation password")
            return render(request,'changepassword.html',{'ml':one})
    return render(request,'changepassword.html')
