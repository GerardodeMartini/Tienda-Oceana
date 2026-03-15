from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProductForm, CategoryForm
from django.db.models import Q

import traceback
from django.http import HttpResponse

def product_list(request, category_slug=None):
    try:
        category = None
        products = Product.objects.filter(is_active=True)
        
        # Filter by Brand based on Session Theme
        current_theme = request.session.get('theme', 'ecosystem')
        
        # We'll use a safer approach for categories to avoid complex JOIN issues
        if current_theme in ['oceana', 'heiwa']:
            brand_q = Q(brand=current_theme) | Q(brand='both')
            products = products.filter(brand_q)
            # Find categories that have at least one product matching this brand
            categories = Category.objects.filter(products__is_active=True).filter(Q(products__brand=current_theme) | Q(products__brand='both')).distinct()
        else:
            categories = Category.objects.filter(products__is_active=True).distinct()
        
        has_offers = products.filter(is_on_sale=True).exists()
        
        if category_slug:
            if category_slug == 'off':
                from django.urls import reverse, NoReverseMatch
                try:
                    current_ns = request.resolver_match.namespace if (request.resolver_match and request.resolver_match.namespace) else 'store'
                    offer_url = reverse(f'{current_ns}:product_list_by_category', args=['off'])
                except:
                    offer_url = f"/{current_theme}/category/off/" if current_theme != 'ecosystem' else "/store/category/off/"

                class MockCategory:
                    def __init__(self, name, slug, url):
                        self.name = name
                        self.slug = slug
                        self.url = url
                    def get_absolute_url(self):
                        return self.url
                        
                category = MockCategory(name="Tesoros en Oferta", slug="off", url=offer_url)
                products = products.filter(is_on_sale=True)
            else:
                category = get_object_or_404(Category, slug=category_slug)
                products = products.filter(category=category)
            
        return render(request, 'store/product/list.html', {
            'category': category,
            'categories': categories,
            'products': products,
            'has_offers': has_offers
        })
    except Exception as e:
        return HttpResponse(f"Error detectado en product_list: {str(e)}<br><pre>{traceback.format_exc()}</pre>", status=500)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'store/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})

@staff_member_required
def seller_dashboard(request):
    products = Product.objects.all().order_by('-id') # Newest first matches creation flow better
    
    # Simple Stats
    total_products = products.count()
    low_stock = products.filter(stock__lte=5).count()
    total_value = sum(p.price * p.stock for p in products) # More accurate value calculation too

    return render(request, 'store/dashboard.html', {
        'products': products,
        'total_products': total_products,
        'low_stock': low_stock,
        'total_value': total_value
    })

@staff_member_required
def product_create(request):
    initial_data = {}
    title = 'Nuevo Producto'
    
    # Handle Combo Context
    if request.GET.get('type') == 'combo':
        title = 'Nuevo Combo / Kit'
        initial_data['brand'] = 'both'
        initial_data['is_combo'] = True
        initial_data['description'] = 'Incluye: \n- '
        
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            # Auto-generate slug from title if not handled by model save
            from django.utils.text import slugify
            import uuid
            
            base_slug = slugify(product.title)
            product.slug = base_slug
            
            # Simple collision check
            if Product.objects.filter(slug=product.slug).exists():
                product.slug = f'{base_slug}-{uuid.uuid4().hex[:6]}'
                
            product.save()
            
            # Handle Gallery Images
            from .models import ProductImage
            for f in request.FILES.getlist('gallery_images'):
                ProductImage.objects.create(product=product, image=f)
                
            return redirect('store:seller_dashboard')
    else:
        form = ProductForm(initial=initial_data, user=request.user)
    
    return render(request, 'store/product_edit.html', {'form': form, 'title': title})

@staff_member_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        if form.is_valid():
            form.save()
            
            # Handle Gallery Images
            from .models import ProductImage
            for f in request.FILES.getlist('gallery_images'):
                ProductImage.objects.create(product=product, image=f)
                
            return redirect('store:seller_dashboard')
    else:
        form = ProductForm(instance=product, user=request.user)
    
    return render(request, 'store/product_edit.html', {'form': form, 'product': product, 'title': f'Editar {product.title}'})

@staff_member_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            from django.utils.text import slugify
            category.slug = slugify(category.name)
            category.save()
            # Redirect back to where they came from if possible, or dashboard
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('store:seller_dashboard')
    else:
        form = CategoryForm()
    
    return render(request, 'store/category_create.html', {'form': form})

@staff_member_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
    return redirect('store:seller_dashboard')

from .models import ProductImage

@staff_member_required
def product_image_delete(request, image_id):
    image = get_object_or_404(ProductImage, id=image_id)
    product_id = image.product.id
    if request.method == 'POST':
        image.delete()
    return redirect('store:product_edit', product_id=product_id)
