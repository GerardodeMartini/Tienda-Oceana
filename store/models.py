from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Nombre')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug / URL')
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Categoría')
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(blank=True, verbose_name='Descripción')
    image = models.ImageField(upload_to='products/', default='products/default.png', verbose_name='Imagen', blank=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug / URL') # Adding unique limit for better urls
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    is_on_sale = models.BooleanField(default=False, verbose_name='En Oferta')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Actualizado')
    
    BRAND_CHOICES = (
        ('oceana', 'Océana'),
        ('heiwa', 'Heiwa'),
        ('both', 'Ambos (Ecosistema)'),
    )
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES, default='both', verbose_name='Marca del Producto')
    
    # Combo specific fields
    is_combo = models.BooleanField(default=False, verbose_name='Es Combo/Kit')
    components = models.ManyToManyField('self', blank=True, symmetrical=False, verbose_name='Productos del Combo')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Image for {self.product.title}"
