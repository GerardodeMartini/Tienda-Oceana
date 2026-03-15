from django import template
from store.models import Product

register = template.Library()


@register.simple_tag
def brand_name_from_value(value: str) -> str:
    """
    Given a brand code ('oceana', 'heiwa', 'both'), return the human-readable label.
    Falls back to the raw value if not found.
    """
    if not value:
        return ""
    mapping = dict(Product.BRAND_CHOICES)
    return mapping.get(value, value)


@register.simple_tag(takes_context=True)
def current_theme_brand_name(context) -> str:
    """
    Returns a displayable brand name based on the current session theme.
    - 'oceana' -> 'Océana'
    - 'heiwa'  -> 'Heiwa'
    - anything else -> 'Océana & Heiwa'
    Useful for SEO titles where you want to show the active brand or the ecosystem.
    """
    request = context.get("request")
    if not request:
        return "Océana & Heiwa"

    theme = getattr(request, "session", {}).get("theme")

    if theme == "oceana":
        return "Océana"
    if theme == "heiwa":
        return "Heiwa"
    return "Océana & Heiwa"

