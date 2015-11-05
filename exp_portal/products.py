from django.shortcuts import render, redirect
from op_tasks.models import Product, Dataset
from django.contrib.auth.decorators import login_required
from tasks import user_authorized
from django.contrib.auth.decorators import login_required
from xdata.settings import LOGIN_URL


@login_required(login_url=LOGIN_URL)
def view_products(request):
	if user_authorized(request):
		products = Product.objects.all()
		return render(request, 'products.html', {'products': products})


@login_required(login_url=LOGIN_URL)
def view_product_details(request, productname):
	if user_authorized(request):
		product = Product.objects.all().filter(name=productname)[0]
		datasets = Dataset.objects.all()
		return render(request, 'product_details.html', {'product': product, 'datasets': datasets})



@login_required(login_url=LOGIN_URL)
def edit_product(request, productpk):
	if user_authorized(request):
		product = Product.objects.get(id=productpk)
		product.name = request.POST['product_name']
		product.team = request.POST['product_team']
		product.url = request.POST['product_url']
		product.instructions = request.POST['instructions_url']
		product.version = request.POST['version']
		product.is_active = request.POST.get('is_active', False)

		# TODO error checking on this, though it should never fail
		dataset = Dataset.objects.all().filter(name=request.POST['dataset'])[0]
		product.dataset = dataset

		product.save()

		return redirect('exp_portal:view_products')


@login_required(login_url=LOGIN_URL)
def manage_products(request):
	if user_authorized(request):
		products = Product.objects.all()
		return render(request, 'products.html', {'products': products})


@login_required(login_url=LOGIN_URL)
def add_product(request):
	if user_authorized(request):
		datasets = Dataset.objects.all()
		return render(request, 'add_product.html', {'datasets': datasets})


@login_required(login_url=LOGIN_URL)
def new_product(request):
	if user_authorized(request):
		product = Product(name=request.POST['product_name'])
		product.url = request.POST['product_url']
		product.team = request.POST['product_team']
		product.url = request.POST['product_url']
		product.version = request.POST['product_version']
		product.instructions = request.POST['product_instructions']
		product.is_active = request.POST.get('product_active', False)

		dataset = Dataset.objects.get(name=request.POST['product_dataset'])
		product.dataset = dataset

		product.save()

		return redirect('exp_portal:view_products')
