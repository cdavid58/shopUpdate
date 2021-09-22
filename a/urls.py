from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^$',index,name="index"),
		url(r'^category/$',category,name="category"),
		url(r'^cart/$',cart,name="cart"),
		url(r'^login/$',login,name="login"),
		url(r'^contact/$',contact,name="contact"),
		url(r'^checkout/$',checkout,name="checkout"),
		url(r'^confirmation/$',confirmation,name="confirmation"),
		url(r'^singleproduct/(\d+)/$',singleproduct,name="singleproduct"),
		url(r'^cart_add/$',cart_add,name="cart_add"),
		url(r'^logout/$',logout,name="logout"),
	]