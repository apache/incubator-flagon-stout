from django.shortcuts import render
from op_tasks.models import UserProfile, Product, Dataset, OpTask

# Create your views here.

def home_page(request):
    if request.user.is_staff:
        return render(request, 'developerhome.html')

def view_dev_status(request):
    if request.user.is_staff:
        userprofiles = UserProfile.objects.all()
        products = Product.objects.all()
        datasets = Dataset.objects.all()
        optasks = OpTask.objects.all()
        return render(request, 'status.html', {'userprofiles': userprofiles, 'products': products, 'datasets': datasets,'optasks': optasks})

def view_dev_products(request):
    if request.user.is_staff:
        products = Product.objects.all()
        return render(request, 'dev_products.html', {'products': products})

def submit_product(request):
    if request.user.is_staff:
        return render(request, 'submit_product.html')

def newProduct(request):
    if request.user.is_staff:
        dataset = Dataset.objects.create(name=request.POST['product_dataset'])
        Product.objects.create(dataset=dataset,
            url=request.POST['product_url'],
            team=request.POST['product_team'],
            name=request.POST['product_name'],
            version=request.POST['product_version'],
            instructions=request.POST['product_instructions'])
        return redirect('/developer/product_comp/')

def product_comp(request):
    if request.user.is_staff:
        return render(request, 'product_comp.html')