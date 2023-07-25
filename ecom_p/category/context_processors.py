from .models import Category
from .models import Brand


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

def brand_links(request):
    brands = Brand.objects.all
    return dict(brands=brands)

