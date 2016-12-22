from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import Products, Image, Images, Orders, Categories, OrderProduct, BillingAddress, ShippingAddress
from django.http import JsonResponse
from .forms import UploadFileForm
import math
# Create your views here.

def index(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
        items = Products.objects.all()
        for item in items:
            pk = str(item.id)
            quantity = {'quantity':1}
            request.session['cart'][pk]=quantity

    print request.session['cart']
    return render(request, 'ecommerce/index.html')
    # url(r'^products/category/(?P<category>\d+)/(?P<categorypage>\d+)$', views.product

    # Left side bar
    categories = Categories.objects.all()
    # Products for specific category
    # products = Products.objects.filter(category=category)
    # Image for product
    # images = Image.objects.filter(product__category_id=category)
    context = {
        # 'categorypage': categorypage,
        'categories': categories,
        # 'products': products,
    }
    return render(request, 'ecommerce/index.html', context)

def browse(request, category, categorypage):
    # url(r'^products/category/(?P<category>\d+)/(?P<categorypage>\d+)$', views.product
    # Left side bar
    categories = Categories.objects.all()
    # Add image example
    # Images.objects.create(product_id=9, image='ecommerce/img/adventure-cat.png', main=True)
    # Products for specific category
    # Specify start and end of a series of product to display on the page
    product_start = (int(categorypage)-1)*15
    product_end = (int(categorypage))*15
    products = Products.objects.filter(category=category).filter(ongoing=True)
    # products1s = Products.objects.filter(category=category)[product_start:product_end-14]
    # products2s = Products.objects.filter(category=category)[product_start+5:product_end-9]
    # products3s = Products.objects.filter(category=category)[product_start+10:product_end-4]
    # products1 = Products.objects.filter(category=category)[product_start+1:product_end-10]
    # products2 = Products.objects.filter(category=category)[product_start+6:product_end-5]
    # products3 = Products.objects.filter(category=category)[product_start+11:product_end]
    productsout = Products.objects.filter(category=category).filter(ongoing=True)[product_start:product_end]
    # Image (big image only) for product
    images = Image.objects.filter(product__category_id=category)

    # Max page needed to display products in a category
    maxpages = math.ceil(len(products)/15.0)
    context = {
        'maxpages': int(maxpages),
        'category': int(category),
        'categorypage': categorypage,
        'prevpage': int(categorypage)-1,
        'nextpage': int(categorypage)+1,
        'categories': categories,
        'images': images,
        # 'products1': products1,
        # 'products2': products2,
        # 'products3': products3,
        # 'products1s': products1s,
        # 'products2s': products2s,
        # 'products3s': products3s,
        'productsout': productsout,
    }
    return render(request, 'ecommerce/browse.html', context)

def product(request, product_id):
    product = Products.objects.get(id=product_id)
    images = len(Image.objects.filter(product_id=product_id))
    main_image1 = Image.objects.filter(product_id=product_id)
    main_image_rest = Image.objects.filter(product_id=product_id)[0:5]
    print Image.objects.filter(product_id=product_id)
    category = product.category.id
    related_product = Products.objects.filter(category_id=category).filter(ongoing=True).exclude(id=product_id)[0:6]
    related_image = Image.objects.filter(product__category_id=category)


    context = {
        'product': product,
        'main_image_1': main_image1,
        'main_image_rest': main_image_rest,
        'related': related_product,
        'related_image': related_image,
    }
    return render(request, 'ecommerce/product.html', context)

def admin(request):
    return render(request, 'ecommerce/admin.html')

def orders(request):
    context ={
        'orders': Orders.objects.all(),
        'billings': BillingAddress.objects.all()
    }
    return render(request, 'ecommerce/orders.html', context)

#dummy creation button#
def testcreate(request):
    category = Categories.objects.get(id=1)

    new_product = Products.objects.create(product = 'Jameson', price = 19.99, quantity = 2, description = 'whiskey', inventory=1, ongoing=True, category=category)

    new_product2 = Products.objects.create(product = 'Heineken', price = 23.99, quantity = 3, description = 'beer', inventory=1, ongoing=True, category=category)

    quantity= new_product.quantity
    price = new_product.price

    quantity2= new_product2.quantity
    price2 = new_product2.price


    total = Products.objects.cost_product(quantity=quantity, price=price)
    total2 = Products.objects.cost_product(quantity=quantity2, price=price2)

    new_order = Orders.objects.create(total=total+total2)

    new_orderproduct = OrderProduct.objects.create(order_product=new_order, product_order = new_product)

    new_orderproduct2 = OrderProduct.objects.create(order_product=new_order, product_order = new_product2)

    billing = BillingAddress.objects.create(first_name='eric', last_name='pan', address='123 fake street', city = 'burbank', state = 'CA', zipcode='91232', order = new_order)
    shipping = ShippingAddress.objects.create(first_name='erica', last_name='tan', address='4321 real street', city = 'los angeles', state = 'CA', zipcode='91232', order = new_order)
    return redirect('orders')

def productcost(quantity, price):
    return quantity*price

def products(request):
    products = Products.objects.all().filter(ongoing=True)
    categories = Categories.objects.all()
    upload = UploadFileForm()
    for product in products:
        for img in product.imagetoproduct.all():
            print img.image
    context = {
            'products': products,
            'categories': categories,
            'upload': upload
            }
    return render(request, 'ecommerce/products.html', context)

def show(request, id):
    order_id = Orders.objects.get(id=id)
    context ={
        'orders' : Orders.objects.get(id=id),
        'shipping': ShippingAddress.objects.get(order=order_id),
        'billing': BillingAddress.objects.get(order=order_id),
        'orderproduct': OrderProduct.objects.filter(order_product=order_id)
    }
    return render(request, 'ecommerce/show.html', context)

def test(request):
    return render(request, 'ecommerce/test.html')

def add_product(request):
    product = Products.objects.add_product(form_data=request.POST)
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        new_image = Image.objects.create(title=form.cleaned_data['title'],image=form.cleaned_data['image'],product=product)
    else:
        print False
    return redirect(reverse('products'))

def update(request):
    orderid = int(request.GET['orderid'])
    status= str(request.GET['status'])
    Orders.objects.update_status(id=orderid, form_data=status)
    new_status= Orders.objects.get(id=orderid)
    return redirect('orders')

def updatetest(request):
    print request.GET
    return HttpResponse()

def delete(request, id):
    product = Products.objects.get(id=id)
    product.ongoing = False
    product.save()
    return redirect(reverse('products'))

def edit(request, id):
    edit_product = Products.objects.edit_product(id=id, form_data=request.POST)
    return redirect(reverse('products'))

def delete_category(request):
    category_id = request.GET['category_id']
    delete_category = Categories.objects.get(id=category_id)
    delete_category.delete()
    return JsonResponse({'response':True})

def cart(request):
    goods = {}
    grandtotal=0
    for value, item in request.session['cart'].iteritems():
        good = Products.objects.get(pk=int(value))
        total = 25.00* float(item['quantity'])
        grandtotal += total
        my_list = {
                    'name':good.product,
                    'description':good.description,
                    'price':25.00,
                    'quantity':item['quantity'],
                    'total':total,
                    'id':good.id
                    }
        pk = str(good.id)
        goods[pk]=my_list
    return render(request, 'ecommerce/cart.html', {'goods':goods, 'grandtotal':grandtotal})

def more(request, id):
    for value, item in request.session['cart'].iteritems():
        if int(id) == int(value):
            item['quantity'] = request.POST['select']
    return redirect('cart')


def ship(request):
    return render(request, 'ecommerce/ship.html')

<<<<<<< HEAD
def remove_from_cart(request, id):
    key = str(id)
    del request.session['cart'][key]
    return redirect('cart')

def card(request):
    return render(request, 'ecommerce/card.html')
=======
def add_cart(request, product_id):
    return redirect(reverse('products'))
>>>>>>> master
