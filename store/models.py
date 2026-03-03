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

    def save(self, *args, **kwargs):
        if self.image and self.image.name != 'products/default.png':
            # Check if image is new or has changed
            is_new_image = False
            if not self.pk:
                is_new_image = True
            else:
                try:
                    old_obj = Product.objects.get(pk=self.pk)
                    if old_obj.image != self.image:
                        is_new_image = True
                except Product.DoesNotExist:
                    is_new_image = True

            if is_new_image:
                try:
                    img = Image.open(self.image)
                    
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
                    
                    output = BytesIO()
                    img.save(output, format='JPEG', quality=85, optimize=True)
                    output.seek(0)
                    
                    # Prevent changing the default.png name accidentally
                    name_parts = self.image.name.split('.')
                    new_name = name_parts[0] if len(name_parts) > 0 else 'image'
                    
                    self.image = InMemoryUploadedFile(
                        output,
                        'ImageField',
                        f"{new_name}.jpg",
                        'image/jpeg',
                        sys.getsizeof(output),
                        None
                    )
                except Exception as e:
                    print(f"Error compressing Product image: {e}")
                    
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title

import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Image for {self.product.title}"

    def save(self, *args, **kwargs):
        if self.image:
            # Check if image is new or has changed
            is_new_image = False
            if not self.pk:
                is_new_image = True
            else:
                try:
                    old_obj = ProductImage.objects.get(pk=self.pk)
                    if old_obj.image != self.image:
                        is_new_image = True
                except ProductImage.DoesNotExist:
                    is_new_image = True

            if is_new_image:
                try:
                    img = Image.open(self.image)
                    
                    # Convert to RGB if needed (e.g. RGBA pngs)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # Resize to max 1000x1000 maintaing aspect ratio
                    img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
                    
                    output = BytesIO()
                    # Save as WebP for optimal compression, fallback to JPEG
                    img.save(output, format='JPEG', quality=85, optimize=True)
                    output.seek(0)
                    
                    # Change the file name to ensure it has correct extension if we wanted, 
                    # but simple compression on the same filename is safer for now
                    self.image = InMemoryUploadedFile(
                        output,
                        'ImageField',
                        f"{self.image.name.split('.')[0]}.jpg",
                        'image/jpeg',
                        sys.getsizeof(output),
                        None
                    )
                except Exception as e:
                    print(f"Error compressing ProductImage: {e}")
                    
        super().save(*args, **kwargs)
