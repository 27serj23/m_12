from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib import messages
from .services import get_products_with_category, get_product_by_id, get_categories
from .forms import ContactForm, ReviewForm


def product_list(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            messages.success(request, f'Спасибо, {review.author_name}! Ваш отзыв на товар "{review.product.name}" сохранён.')
            return redirect('product_list')
    else:
        form = ReviewForm()

    products = get_products_with_category(count=None, in_stock_only=False)
    categories = get_categories()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'form': form,
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


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'store/contact.html', {'form': form})