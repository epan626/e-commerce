from django.shortcuts import render, redirect, reverse
from .models import Products, Categories
from django.http import JsonResponse

# Create your views here.

def index(request):
    return render(request, 'ecommerce/index.html')

def product(request):
    return render(request, 'ecommerce/product.html')

def admin(request):
    return render(request, 'ecommerce/admin.html')

def orders(request):
    return render(request, 'ecommerce/orders.html')

def products(request):
    products = Products.objects.all().filter(ongoing=True)
    categories = Categories.objects.all()
    context = {
            'products': products,
            'categories': categories
            }
    return render(request, 'ecommerce/products.html', context)

def show(request):
    return render(request, 'ecommerce/show.html')

def test(request):
    return render(request, 'ecommerce/test.html')

def add_product(request):
    product = Products.objects.add_product(form_data=request.POST)
    return redirect(reverse('products'))

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
