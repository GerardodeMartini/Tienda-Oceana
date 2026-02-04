
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category
from django.utils.text import slugify

categories = [
    "Línea Capilar",
    "Línea Sentidos",
    "Línea Maquillaje Botánico",
    "Línea Higiene",
    "Botiquín Natural",
    "% OFF"
]

print("Creating categories...")
for name in categories:
    slug = slugify(name)
    cat, created = Category.objects.get_or_create(
        name=name,
        defaults={'slug': slug}
    )
    if created:
        print(f"✅ Created: {name}")
    else:
        print(f"ℹ️ Exists: {name}")

print("Done!")
