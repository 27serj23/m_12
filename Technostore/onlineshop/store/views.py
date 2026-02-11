from django.shortcuts import render
from django.http import Http404
from .services import get_products_with_category, get_product_by_id, get_categories


def product_list(request):
    products = get_products_with_category(count=None, in_stock_only=False)
    categories = get_categories()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, product_id):
    product = get_product_by_id(product_id)
    if not product:
        raise Http404("Товар не найден")
    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)


def home(request):
    products = get_products_with_category(count=6)
    categories = get_categories(count=4)
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)
