from __future__ import unicode_literals
import unicodedata
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def validate_registration(self, form):
		errors = []
		if len(form['first_name']) == 0:
			errors.append("First Name is required")
		elif len(form['first_name']) < 3:
			errors.append("First Name must be atleast 3 characters")
		elif not form['first_name'].isalpha():
			errors.append("First Name must only consist of letters")

		if len(form['last_name']) == 0:
			errors.append("Last Name is required")
		elif len(form['last_name']) < 3:
			errors.append("Last Name must be atleast 3 characters")
		elif not form['last_name'].isalpha():
			errors.append("Last Name must only consist of letters")

		if len(form['email']) == 0:
			errors.append("Email is required")
		elif not EMAIL_REGEX.match(form['email']):
			errors.append("Please enter a valid email address")
		elif User.objects.filter(email=form['email']):
			errors.append("Account already exist for that email")

		if len(form['password']) == 0:
			errors.append("Password is required")
		elif len(form['password']) < 0:
			errors.append("Password must has atleast 8 characters")

		if form['passwordcf'] != form['password']:
			errors.append("Password confirmation does not match")

		return errors

	def register(self, form):
		hashed_pass = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
		return self.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=hashed_pass)

	def login_check(self, form):
		check_user = self.filter(email=form['email'])
		if check_user:
			user = check_user[0]
			if bcrypt.hashpw(form['password'].encode(), user.password.encode()) == user.password:
				return user
		return None

class Users(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	added_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class CategoryManager(models.Manager):
	def retrieve_category(self, category_name):
		try:
			category = Categories.objects.get(category=category_name)
			return category
		except:
			new_category = Categories.objects.create(category=category_name)
			return new_category

class Categories(models.Model):
	category = models.CharField(max_length=30)
	objects = CategoryManager()

class ProductManager(models.Manager):
	def add_product(self, form_data):
		if form_data['category'] == 'default' and len(form_data['new_category']):
			category = Categories.objects.create(category=form_data['new_category'])
			new_product = Products.objects.create(product=form_data['name'], description=form_data['description'], inventory=form_data['inventory'], ongoing=True, category=category, price=form_data['price'])
		else:
			category = Categories.objects.retrieve_category(category_name=form_data['category'])
			new_product = Products.objects.create(product=form_data['name'], description=form_data['description'], inventory=form_data['inventory'], ongoing=True, category=category, price=form_data['price'])
		return new_product

	def edit_product(self, id, form_data):
		product = Products.objects.get(id=id)
		product.product = form_data['name']
		product.description = form_data['description']
		product.inventory = form_data['inventory']
		try:
			price = float(form_data['price'])
		except:
			price = 0
		if price != 0:
			product.price = form_data['price']
		else:
			product.price = 0
		if form_data['category'] != 'default':
			category = Categories.objects.retrieve_category(category_name=form_data['category'])
			product.category = category
		elif len(form_data['new_category']):
			new_category = Categories.objects.create(category=form_data['new_category'])
			product.category = new_category
		product.save()
		return product
	def cost_product(self, quantity, price):
		return quantity*price

class OrdersManager(models.Manager):
	def update_status(self, id, form_data):
		return Orders.objects.filter(pk=id).update(status=form_data)

class Image(models.Model):
	title = models.CharField(max_length=100, null=True)
	image = models.FileField(upload_to = "apps/ecommerce/static/ecommerce/img", default ="admin_app/img/img.jpg")
	product = models.ForeignKey('Products', related_name='imagetoproduct')

class Products(models.Model):
	product = models.CharField(max_length=30)
	price = models.DecimalField(max_digits=5, decimal_places=2, default = 20.00)
	quantity = models.PositiveSmallIntegerField(default=0)
	description = models.CharField(max_length=255)
	inventory = models.PositiveSmallIntegerField(default=0)
	price = models.FloatField(null=True)
	ongoing = models.CharField(max_length=5)
	category = models.ForeignKey('Categories', models.DO_NOTHING, related_name="productofcategory")
	objects = ProductManager()

class Images(models.Model):
	image = models.CharField(max_length=255)
	product = models.ForeignKey('Products', models.DO_NOTHING, related_name="imageofproduct")

class Orders(models.Model):
	total = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	tax = models.DecimalField(max_digits=2, decimal_places=2, null=True, default =.09)
	shipping = models.DecimalField(max_digits=3, decimal_places=2, null=True, default =5.00)
	status = models.CharField(max_length=30, null=True, default = 'Order in Process')
	added_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = OrdersManager()

class OrderProduct(models.Model):
	order_product = models.ForeignKey('Orders', models.DO_NOTHING, related_name="ordersofproduct")
	product_order = models.ForeignKey('products', models.DO_NOTHING, related_name="productoforder")

class BillingAddress(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=30)
	state = models.CharField(max_length=30)
	zipcode = models.CharField(max_length=30)
	order = models.ForeignKey('Orders', models.DO_NOTHING, related_name="billoforder")

class ShippingAddress(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=30)
	state = models.CharField(max_length=30)
	zipcode = models.CharField(max_length=30)
	order = models.ForeignKey('Orders', models.DO_NOTHING, related_name="shipoforder")
