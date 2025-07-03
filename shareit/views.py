# from django.http import HttpResponse

# def home(request) :
#     return HttpResponse("<h1>Hello home</h1>")

# def about(request) :
#     return HttpResponse("<h1>Hello about</h1>")

# def contact(request) :
#     return HttpResponse("<h1>Hello contact</h1>")

# def service(request) :
#     return HttpResponse("<h1>Hello service</h1>")

# def register(request) :
#     return HttpResponse("<h1>Hello register</h1>")

# def login(request) :
#     return HttpResponse("<h1>Hello login</h1>")

from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage


from . import models
from . import emailAPI
import time

def home(request) :
    return render(request,"home.html")

def about(request) :
    return render(request,"about.html")

def contact(request) :
    return render(request,"contact.html")

def service(request) :
    return render(request,"service.html")

    
def register(request):
    if request.method=="GET":    
        return render(request,"register.html",{"output":""})
    else:
        #to recieve from data
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")
        print(gender)

        # to insert record in database
        p=models.Register(name=name,email=email,password=password,mobile=mobile,address=address,city=city,gender=gender,status=0,role="user",info=time.asctime())
        p.save()

        # to send mail using api
        emailAPI.sendMail(email,password)

        return render(request,"register.html",{"output":"User register successfully...."}) 

def verify(request):
    vemail=request.GET.get("vemail")
    models.Register.objects.filter(email=vemail).update(status=1)        
    return redirect("/login/")
           


def login(request) :
    if request.method=="GET":
        return render(request,"login.html",{"output":""})
    else:
        #recieve data for login
        email=request.POST.get("email")
        password=request.POST.get("password")
        # return render(request,"login.html",{"output":"login successfully......."})

        #to match user details in database
        userDetails=models.Register.objects.filter(email=email,password=password,status=1)

        if len(userDetails)>0:
            #to store user details in session
            request.session["sunm"]=userDetails[0].email
            request.session["srole"]=userDetails[0].role

            print(userDetails[0].role)    # to get user role
            if userDetails[0].role=="admin":
                return redirect("/myadmin/")
            else:
                return redirect("/user/")
            # return render(request,"login.html",{"output":"login success"})
        else:
            return render(request,"login.html",{"output":"Invalid user or verify your account...."})                        

def adminhome(request) :
    return render(request,"adminhome.html",{"sunm":request.session["sunm"]})
    

def userhome(request) :
    return render(request,"userhome.html",{"sunm":request.session["sunm"]})


def manageusers(request):

    #to fetch user details
    userDetails=models.Register.objects.filter(role="user")

    return render(request,"manageusers.html",{"userDetails":userDetails,"sunm":request.session["sunm"]})

def manageuserstatus(request):
    #to get status data from url
    s=request.GET.get("s")
    regid=int(request.GET.get("regid"))

    if s=="active":
        models.Register.objects.filter(regid=regid).update(status=1)
    elif s=="inactive":
        models.Register.objects.filter(regid=regid).update(status=0)    
    else:
        models.Register.objects.filter(regid=regid).delete()

    return redirect("/manageusers/")

def sharenotes(request) :
    if request.method=="GET":
        return render(request,"sharenotes.html",{"sunm":request.session["sunm"],"output":""})
    else:
        #to recieve data from UI
        title=request.POST.get("title")
        category=request.POST.get("category")
        description=request.POST.get("description")

        #to recieve file from UI & to push in media folder
        files=request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(files.name,files)

        p=models.Sharenotes(title=title,category=category,description=description,filename=filename,uid=request.session["sunm"],info=time.asctime())

        p.save()

        return render(request,"sharenotes.html",{"sunm":request.session["sunm"],"output":"Content uploaded successfully...."})            


def viewnotes(request):
    data=models.Sharenotes.objects.all()
    return render(request,"viewnotes.html",{"sunm":request.session["sunm"],"data":data})


def funds(request):
    paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
    paypalID="sb-tuxhw43008525@business.example.com"
    amt=100
    return render(request,"funds.html",{"sunm":request.session["sunm"],"paypalURL":paypalURL,"paypalID":paypalID,"amt":amt})


def payment(request):
    uid=request.GET.get("uid")
    amt=request.GET.get("amt")
    p=models.Payment(uid=uid,amt=amt,info=time.asctime())
    p.save()
    return redirect("/success/")

def success(request):
    return render(request,"success.html",{"sunm":request.session.get("sunm")})

def cancel(request):
    return render(request,"cancel.html",{"sunm":request.session["sunm"]}) 


def cpadmin(request):
    if request.method=="GET":
        return render(request,"cpadmin.html",{"sunm":request.session["sunm"],"output":""})
    else:
        #to get data from form
        email=request.session["sunm"]
        opassword=request.POST.get("opassword")
        npassword=request.POST.get("npassword")
        cnpassword=request.POST.get("cnpassword")
        
        #to check old password is valid or not
        userDetails=models.Register.objects.filter(email=email,password=opassword)
        if len(userDetails)>0:
            if npassword==cnpassword:
                models.Register.objects.filter(email=email).update(password=cnpassword)
                return render(request,"cpadmin.html",{"sunm":request.session["sunm"],"output":"Password changes successfully...."})    
            else:    
                return render(request,"cpadmin.html",{"sunm":request.session["sunm"],"output":"New & Confirm new password mismatch...."})                
        else:
            return render(request,"cpadmin.html",{"sunm":request.session["sunm"],"output":"Invalid old password , please try again...."})


def cpuser(request):
    if request.method=="GET":
        return render(request,"cpuser.html",{"sunm":request.session["sunm"],"output":""})
    else:
        #to get data from form
        email=request.session["sunm"]
        opassword=request.POST.get("opassword")
        npassword=request.POST.get("npassword")
        cnpassword=request.POST.get("cnpassword")
        
        #to check old password is valid or not
        userDetails=models.Register.objects.filter(email=email,password=opassword)
        if len(userDetails)>0:
            if npassword==cnpassword:
                models.Register.objects.filter(email=email).update(password=cnpassword)
                return render(request,"cpuser.html",{"sunm":request.session["sunm"],"output":"Password changes successfully...."})    
            else:    
                return render(request,"cpuser.html",{"sunm":request.session["sunm"],"output":"New & Confirm new password mismatch...."})                
        else:
            return render(request,"cpuser.html",{"sunm":request.session["sunm"],"output":"Invalid old password , please try again...."})


def epadmin(request):
    email=request.session["sunm"]
    userDetails=models.Register.objects.filter(email=email)

    m,f="",""
    if userDetails[0].gender=="male":
        m="checked"
    else:        
        f="checked"

    if request.method=="GET":
        return render(request,"epadmin.html",{"sunm":email,"user":userDetails[0],"output":"","m":m,"f":f})
    else:
        #to get edited content
        name=request.POST.get("name")
        email=request.POST.get("email")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        #to update data in database
        models.Register.objects.filter(email=email).update(name=name,mobile=mobile,address=address,city=city,gender=gender)

        return redirect("/epadmin/")
