from django.http import HttpResponseRedirect
from decimal import Decimal
from django.conf import settings
from datetime import datetime
from django.db import models
from datetime import date

class Client(models.Model):
	firstname = models.CharField(max_length=20)
	lastname = models.CharField(max_length=20)
	phone = models.CharField(max_length=10)
	email = models.EmailField()
	address = models.TextField()
	note = models.TextField(blank=True,null=True)
	password = models.CharField(max_length=18,null=True)

	def __str__(self):
		return self.email


class Category(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=150,default="Camisas")
	price = models.CharField(max_length=10,default=0)
	description = models.TextField(default="Camisas 100% Personalizadas")
	image = models.ImageField(upload_to = "product")
	new = models.BooleanField(default=True)
	oferta = models.CharField(max_length=3,default=0)
	category = models.ForeignKey(Category,on_delete = models.CASCADE)

	def __str__(self):
		return self.name+" - "+self.category.name


	def discount(self):
		value = float(self.price) - ( float(self.price) * ( float(self.oferta) / 100 ) )
		return int(value)



class Consecutive(models.Model):
	number = models.CharField(max_length=10)

class Order(models.Model):
	consecutive = models.CharField(max_length=10)
	article = models.CharField(max_length=150)
	price = models.CharField(max_length=10)
	quanty = models.CharField(max_length=10)
	discount = models.CharField(max_length=10)
	total = models.CharField(max_length=20)
	recived = models.BooleanField(default=False)
	date = models.CharField(max_length=10,default=date.today())
	client = models.ForeignKey(Client,on_delete=models.CASCADE)

	def __str__(self):
		return "Nº de consecutive --> "+self.consecutive





class Carrito(object):
	def __init__(self,request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart
		self.request = request

	def save(self):
		self.session[settings.CART_SESSION_ID]=self.cart
		self.session.modified = True

	def add(self,product,quanty = 0):
		try:
			self.cart[str(product.pk)]
		except KeyError as e:
			self.request.session['carrito'] += 1
			
		total = float(product.discount()) * float(quanty)
		self.cart[str(product.pk)] = {'code':product.pk,'article':product.name,'quanty':quanty,'price':product.discount(),'discount':product.oferta,'total':total,'image':product.image.url,
											'description':product.description
										}
		self.save()
		print(self.cart)

	def remove(self,product):
		product_id = str(product.pk)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)

		for item in self.cart.values():
			yield item


	def __len__(self):
		return sum(item['quanty'] for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True



