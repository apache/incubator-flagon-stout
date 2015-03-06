from django.shortcuts import render
from op_tasks.models import Participant, Product, Dataset, OpTask

# Create your views here.

def home_page(request):
	return render(request, 'developerhome.html')

def view_status(request):
	participants = Participant.objects.all()
	products = Product.objects.all()
	datasets = Dataset.objects.all()
	optasks = OpTask.objects.all()
	return render(request, 'status.html', {'participants': participants, 'products': products, 'datasets': datasets,'optasks': optasks})

def view_products(request):
	products = Product.objects.all()
	return render(request, 'products.html', {'products': products})	

def submit_product(request):
    return render(request, 'submit_product.html')

def newProduct(request):
    dataset = Dataset.objects.create(name=request.POST['product_dataset'])
    Product.objects.create(dataset=dataset, 
        url=request.POST['product_url'], 
        team=request.POST['product_team'], 
        name=request.POST['product_name'], 
        version=request.POST['product_version'], 
        instructions=request.POST['product_instructions'])
    return redirect('/developer/product_comp/')

def product_comp(request):
    return render(request, 'product_comp.html')