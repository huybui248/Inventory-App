from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from inventory.models import Product
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
def home(request):
    products = Product.objects.all().order_by('-created_at')
    # Đếm số sản phảm
    total_products = products.count()
    # Tính giá trị sản phẩm
    total_values = sum(product.total_value for product in products)
    # Chức năng tìm kiếm
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )

    #Phân trang
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {'total_products': total_products,
               'total_values': total_values,
               'products': page_obj,
               'query': query}
    return render(request, 'inventory/home.html', context)

def add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
    return render(request, 'inventory/add.html')

def inventory(request):
    products = Product.objects.all().order_by('-created_at')
    # Chức năng tìm kiếm
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products': products,
               'products': page_obj,}
    return render(request, 'inventory/inventory.html', context)

def delete(request, id):
    product =get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('home')

def edit(request, id):
    product =get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    #Khi edit thì sẽ hiển thị dữ liệu cũ
    return render(request, 'inventory/add.html',{
    'product': product,
    'is_edit': True
    })
