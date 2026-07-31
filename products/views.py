from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product, Category, Brand
from products.forms import ProductForm, CategoryForm, BrandForm

@login_required
def products_list(request):
    business = request.user.get_business()
    products = Product.objects.filter(business=business)

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    brand_id = request.GET.get('brand')
    if brand_id:
        products = products.filter(brand_id=brand_id)

    categories = Category.objects.filter(business=business)
    brands = Brand.objects.filter(business=business)

    return render(request, 'products/products_list.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
    })


@login_required
def product_create(request):
    business = request.user.get_business()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.business = business
            product.save()
            messages.success(request, f"Product '{product.name}' created successfully.")
            return redirect('products_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {'form': form, 'title': 'Add New Product'})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully.")
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {'form': form, 'title': f'Edit {product.name}', 'product': product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_employee():
        messages.error(request, "Cashiers do not have permission to delete products.")
        return redirect('products_list')

    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' deleted successfully.")
        return redirect('products_list')

    return render(request, 'products/product_confirm_delete.html', {'product': product})


@login_required
def categories_list(request):
    business = request.user.get_business()
    categories = Category.objects.filter(business=business)

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.business = business
            cat.save()
            messages.success(request, "Category added successfully.")
            return redirect('categories_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = CategoryForm()

    return render(request, 'products/categories.html', {'categories': categories, 'form': form})


@login_required
def brands_list(request):
    business = request.user.get_business()
    brands = Brand.objects.filter(business=business)

    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            b = form.save(commit=False)
            b.business = business
            b.save()
            messages.success(request, "Brand added successfully.")
            return redirect('brands_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = BrandForm()

    return render(request, 'products/brands.html', {'brands': brands, 'form': form})
