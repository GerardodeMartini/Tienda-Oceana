from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProductForm, CategoryForm
from django.db.models import Sum, F, Q, Count

def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(is_active=True)
    
    # Filter by Brand based on Session Theme
    current_theme = request.session.get('theme', 'ecosystem')
    # Filter categories that have active products matching the current theme
    category_filter = Q(products__is_active=True)
    if current_theme in ['oceana', 'heiwa']:
        category_filter &= (Q(products__brand=current_theme) | Q(products__brand='both'))
        products = products.filter(Q(brand=current_theme) | Q(brand='both'))
    
    categories = Category.objects.filter(category_filter).distinct()
        
    has_offers = products.filter(is_on_sale=True).exists()
    
    if category_slug:
        if category_slug == 'off':
            class MockCategory:
                name = "Tesoros en Oferta"
                slug = "off"
                
                def get_absolute_url(self):
                    from django.urls import reverse
                    return reverse('store:product_list_by_category', args=['off'])
                    
            category = MockCategory()
            # The brand filter is already applied above to the 'products' queryset!
            # We just need to add the sale filter on top of the already filtered brand products.
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
