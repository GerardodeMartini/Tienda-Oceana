
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Product, Category

def create_product():
    # Category
    category_name = "Botiquín Natural"
    category, _ = Category.objects.get_or_create(name=category_name, defaults={'slug': 'botiquin-natural'})

    # Product Details
    name = "Crema de Tomillo"
    description = """Expectorante & balsámica

fórmula concentrada, a base de aceite medicinal de tomillo, menta y eucaliptus 

textura suave
forma una membrana caliente que asiste en el proceso de descongestión y expectoración,  aliviando la tos y aportando un efecto balsámico 

alivia la sensación de constricción del pecho, calma los catarros producidos por la inflamación de las mucosas disminuyendo la secreción, al mismo tiempo que aumenta la sensación de purificación y bienestar general

excelente aliada para las épocas de frío y viento
creada para toda la familia

contiene 👉 aceite medicinal de tomillo, alcanfor, menta, eucaliptus, magia 
50gr"""
    price = Decimal('13900.00')
    image_path = 'products/crema_tomillo.jpg'

    product, created = Product.objects.get_or_create(
        title=name,
        defaults={
            'description': description,
            'price': price,
            'category': category,
            'image': image_path,
            'slug': 'crema-de-tomillo',
            'stock': 100,  # Default initial stock
            'is_active': True
        }
    )

    if created:
        print(f"✅ Producto creado: {product.title}")
    else:
        print(f"ℹ️ El producto ya existía: {product.title}")
        # Update fields if it existed
        product.description = description
        product.price = price
        product.image = image_path
        product.category = category
        product.save()
        print(f"🔄 Producto actualizado: {product.title}")

if __name__ == '__main__':
    create_product()
