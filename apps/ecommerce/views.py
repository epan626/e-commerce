from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import Products, Orders, Categories, OrderProduct, BillingAddress, ShippingAddress
from django.shortcuts import render, redirect, reverse
from .models import Products, Categories, Image
from django.http import JsonResponse
from .forms import UploadFileForm
# Create your views here.

def index(request):
    return render(request, 'ecommerce/index.html')

def product(request):
    return render(request, 'ecommerce/product.html')

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
    return render(request, 'ecommerce/cart.html')

def ship(request):
    return render(request, 'ecommerce/ship.html')
