from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *

def createData(request):
	if 'carrito' not in request.session:
		request.session['carrito'] = 0

def logout(request):
	del request.session['carrito']
	del request.session['userActive']
	return redirect("/")

def index(request):
	if 'carrito' not in request.session:
		request.session['carrito'] = 0
	product = Product.objects.all()
	category = Category.objects.all()

	return render(request,'index.html',{'product':product,'category':category})


def category(request):
	createData(request)
	category = Category.objects.all()
	product = Product.objects.all()
	return render(request,'Catagori.html',{'product':product,'category':category})

def cart(request):
	createData(request)
	cart = Carrito(request)
	subtotal = 0
	for i in cart:
		subtotal += float(i['total'])

	return render(request,'cart.html',{'cart':cart,'subtotal':subtotal})

def contact(request):
	createData(request)
	return render(request,'contact.html')

def checkout(request):
	createData(request)
	cart = Carrito(request)
	con = Consecutive.objects.get(pk=1)
	if 'userActive' in request.session:
		for i in cart:
			Order(
				consecutive = con.number,
				article = i['article'],
				price = i['price'],
				quanty = i['quanty'],
				discount = i['discount'],
				total = i['total'],
				client = Client.objects.get(email=request.session['userActive'])
			).save()
		request.session['consecutive'] = con.number
		con.number = str(int(con.number) + 1)
		con.save()
		return redirect("/confirmation")

	if request.method == 'POST':
		try:
			client = Client.objects.get(email=request.POST.get("compemailany"))
		except Client.DoesNotExist:
			client = None
		if client is None:
			Client(
				firstname = request.POST.get('name'),
				lastname = request.POST.get('last'),
				phone = request.POST.get('number'),
				email = request.POST.get('compemailany'),
				address = request.POST.get('add1'),
				note = request.POST.get('city'),
				password = request.POST.get('password'),
			).save()

			for i in cart:
				Order(
					consecutive = con.number,
					article = i['article'],
					price = i['price'],
					quanty = i['quanty'],
					discount = i['discount'],
					total = i['total'],
					client = Client.objects.get(email=request.POST.get("compemailany"))
				).save()
			request.session['consecutive'] = con.number
			con.number = str(int(con.number) + 1)
			con.save()
			return redirect("/confirmation")

	subtotal = 0
	for i in cart:
		subtotal += float(i['total'])
	return render(request,'checkout.html',{'cart':cart,'subtotal':subtotal})

def confirmation(request):
	createData(request)
	order = Order.objects.filter(consecutive=request.session['consecutive'])
	order_2 = Order.objects.filter(consecutive=request.session['consecutive']).last()
	print(order)
	subtotal = 0
	for i in order:
		subtotal += float(i.total)

	cart = Carrito(request)
	cart.clear()
	del request.session['carrito']
	del request.session['consecutive']


	return render(request,'confirmation.html',{'order':order,'order_2':order_2,'subtotal':subtotal})


def login(request):
	createData(request)

	if request.method == "POST":
		try:
			client = Client.objects.get(email = request.POST.get("name"), password = request.POST.get("password"))
		except Client.DoesNotExist:
			client = None

		if client is not None:
			request.session['userActive'] = request.POST.get("name")
			return redirect("/")

	return render(request,'login.html')



def singleproduct(request,pk):
	createData(request)
	product = Product.objects.get(pk=pk)
	return render(request,'single-product.html',{'p':product})


def cart_add(request):
	if request.is_ajax():
		p = Product.objects.get(pk=request.GET.get("id"))
		cart = Carrito(request)

		cart.add(p,int(request.GET.get('quanty')))
		return HttpResponse("data")



def cart_remove(request,product):
	if request.is_ajax():
		cart = Carro(request)
		cart.remove(product)
		








