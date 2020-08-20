from django.shortcuts import render, redirect
from.models import Customer, Order, Product, OrderItem, shippingAddress
from django.http import JsonResponse
import json
from.forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
import datetime

# Create your views here.

def loginView(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('store')

	context = {

	}
	return render(request,'store/login.html')

def registerView(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
		form = CreateUserForm()

	context = {
		'form' :form
	}
	return render(request, 'store/register.html', context)

def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, order_complete=False)
		items = order.orderitem_set.all()
		cartitems = order.totalItem
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
		items = []
		order = {
			'totalItem' :0,
			'total_cart_items_price' : 0,
			'shipping': False
		}
		cartitems = order['totalItem']
		for i in cart:
			try:
				cartitems += (cart[i]['quantity'])
				product = Product.objects.get(id=i)
				total = (product.price* cart[i]['quantity'])
				item={
					'product':{
						'id' : product.id,
						'product_name'  : product.product_name,
						'price' : product.price,
						'imageURL' : product.imageURL
						},
					'quantity' : cart[i]['quantity'],
					'totalPrice':total
				}
				items.append(item)
			except:
				pass

			order['total_cart_items_price'] += total
		order['totalItem'] += cartitems

	products = Product.objects.all()
	context = {
		'products' : products,
		'cartitems' : cartitems,
	}
	return render(request, 'store/store.html', context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, order_complete=False)
		items = order.orderitem_set.all()
		cartitems = order.totalItem
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
		items = []
		order = {
			'totalItem' :0,
			'total_cart_items_price' : 0,
			'shipping': False
		}
		cartitems = order['totalItem']
		for i in cart:
			try:
				cartitems += (cart[i]['quantity'])
				product = Product.objects.get(id=i)
				total = (product.price* cart[i]['quantity'])
				item={
					'product':{
						'id' : product.id,
						'product_name'  : product.product_name,
						'price' : product.price,
						'imageURL' : product.imageURL
						},
					'quantity' : cart[i]['quantity'],
					'totalPrice':total
				}
				items.append(item)
			except:
				pass

			order['total_cart_items_price'] += total
		order['totalItem'] += cartitems

		
	context = {
		'items' :items,
		'order' : order,
		'cartitems' : cartitems
	}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, order_complete=False)
		items = order.orderitem_set.all()
		cartitems = order.totalItem
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
		items = []
		order = {
			'totalItem' :0,
			'total_cart_items_price' : 0,
			'shipping': False
		}
		cartitems = order['totalItem']
		for i in cart:
			try:
				cartitems += (cart[i]['quantity'])
				product = Product.objects.get(id=i)
				total = (product.price* cart[i]['quantity'])
				item={
					'product':{
						'id' : product.id,
						'product_name'  : product.product_name,
						'price' : product.price,
						'imageURL' : product.imageURL
						},
					'quantity' : cart[i]['quantity'],
					'totalPrice':total
				}
				items.append(item)
			except:
				pass

			order['total_cart_items_price'] += total
		order['totalItem'] += cartitems

	context = {
		'items' :items,
		'order' : order,
		'cartitems' : cartitems
	}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productid = data['productId']
	action = data['action']
	customer = request.user.customer
	product = Product.objects.get(id=productid)
	order, creared = Order.objects.get_or_create(customer=customer, order_complete=False)
	orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderitem.quantity = (orderitem.quantity + 1)
	elif action == 'remove':
		orderitem.quantity = (orderitem.quantity - 1)

	orderitem.save()

	if orderitem.quantity <= 0:
		orderitem.delete()

	return JsonResponse('Item added here', safe=False)

def processOrder(request):
	print(request.user.customer)
	transaction_id = datetime.datetime.now().timestamp()
	print(transaction_id)
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, order_complete=False)
		total = float(data['form']['total'])
		order.tranction_id = transaction_id

		if total == float(order.total_cart_items_price):
			order.order_complete = True
		order.save()

		if order.shipping == True:
			shippingAddress.objects.create(
				customer = customer,
				order = order,
				address = data['shipping']['address'],
				city = data['shipping']['city'],
				state = data['shipping']['state'],
				zip_code = data['shipping']['zipcode'],
			)
		print(order.orderItem_set.all())
	else:
		print('user not logged in')
	return JsonResponse('order complete', safe=False)