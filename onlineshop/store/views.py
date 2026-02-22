from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib import messages
from .services import get_products_with_category, get_product_by_id, get_categories
from .forms import ContactForm, ReviewForm


def product_list(request):
    """Отображает список товаров с пагинацией и форму для отзыва."""
    products = get_products_with_category(count=None, in_stock_only=False)
    categories = get_categories()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'form': ReviewForm(),  # пустая форма для отображения
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


def create_review(request):
    """Обрабатывает создание отзыва (POST-запросы с формы со страницы списка или отдельной страницы)."""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            messages.success(
                request,
                f'Спасибо, {review.author_name}! Ваш отзыв на товар "{review.product.name}" сохранён.'
            )
            return redirect('product_list')
        else:
            # Если ошибки, сохраняем форму и возвращаем пользователя обратно на страницу, откуда пришёл запрос
            # (обычно это product_list, но может быть и отдельная страница)
            # Для упрощения перенаправим на product_list с сообщением об ошибке
            error_messages = []
            for field, errors in form.errors.items():
                field_label = form.fields[field].label if field in form.fields else field
                error_messages.append(f"{field_label}: {', '.join(errors)}")
            messages.error(request, f"Ошибка в форме: {'; '.join(error_messages)}")
            return redirect('product_list')
    else:
        # GET-запрос — показываем отдельную страницу с формой (опционально)
        initial = {}
        product_id = request.GET.get('product')
        if product_id:
            try:
                product = get_product_by_id(int(product_id))
                if product:
                    initial['product'] = product
            except ValueError:
                pass
        form = ReviewForm(initial=initial)
    return render(request, 'store/create_review.html', {'form': form})