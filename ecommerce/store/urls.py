from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url

	path('', views.store, name="store"),
	path('register/', views.registerView, name='register'),
	path('login/', views.loginView, name='login'),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update/', views.updateItem, name="update"),
	path('process_order/', views.processOrder, name="process_order"),

]