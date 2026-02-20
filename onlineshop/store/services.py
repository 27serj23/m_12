from .models import Product, Category

def get_products_with_category(count: int = 10,
                               in_stock_only: bool = True,
                               category_id: int = None):
    queryset = Product.objects.select_related('category', 'brand').prefetch_related('tags')
    if in_stock_only:
        queryset = queryset.filter(stock__gt=0)
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    if count is None:
        return queryset
    return queryset[:count]


def get_product_by_id(product_id: int) -> Product | None:
    try:
        return Product.objects.select_related('category', 'brand') \
                              .prefetch_related('tags') \
                              .get(id=product_id)
    except Product.DoesNotExist:
        return None


def get_categories(count: int = 10):
    queryset = Category.objects.all()
    if count is None:
        return queryset
    return queryset[:count]