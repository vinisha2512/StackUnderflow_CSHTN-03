"""Medistop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from user import views as user_views
from payment import views as payment_views
from prescription import views as presc_views
from shipment import views as shipment_views
from administrator import views as admin_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.homepage, name="homepage"),
    path('login/', user_views.login, name='login'),
    path('signup/', user_views.signup, name='signup'),
    path('reset', user_views.reset, name='reset'),
    path('logout', user_views.logout, name='logout'),
    path('upload_prescription', presc_views.upload, name="upload"),
    path('uploaded_meds', presc_views.read_presc, name='upload_pres'),
    path("cart", presc_views.cart, name="cart"),
    path('placeOrder', presc_views.placeOrder, name="placeOrder"),
    path("med_details/<str:MEDNAME>", user_views.med_deets, name='med_details'),
    path("<str:category>", user_views.med_class, name='med_class'),
    path('cartpresc/', presc_views.cartpresc, name='cartpresc'),
    url(r'^user/incre/$',presc_views.f1),
    url(r'^user/decre/$',presc_views.f2),
    url(r'^user/del/$',presc_views.delete),
    url(r'^addtocart/$',user_views.addtocart),
    url(r'^', user_views.homepage, name="homepage"),
    #url('nameforurl', user_views.views_function, name='nameforurl'),
]
