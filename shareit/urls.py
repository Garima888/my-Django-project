# from django.contrib import admin
# sb-tuxhw43008525@business.example.com
# sb-zwuko43202166@personal.example.com
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path("",views.home),
    path("about/",views.about),
    path("contact/",views.contact),
    path("service/",views.service),
    path("register/",views.register),
    path("verify/",views.verify),
    path("login/",views.login),
    path("myadmin/",views.adminhome),
    path("user/",views.userhome),
    path("manageusers/",views.manageusers),
    path("manageuserstatus/",views.manageuserstatus),
    path("sharenotes/",views.sharenotes),
    path('viewnotes/', views.viewnotes),
    path('funds/', views.funds),
    path('payment/', views.payment),
    path('success/', views.success),
    path('cancel/', views.cancel),
    path('cpadmin/', views.cpadmin),
    path('cpuser/', views.cpuser),
     path('epadmin/', views.epadmin)
     
     
     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
