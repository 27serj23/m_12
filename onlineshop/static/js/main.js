/**
 * Основной JavaScript файл для TechStore
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('TechStore загружен');

    initCartButtons();
    initAlerts();
    initFormValidation(); // новая функция
});

/**
 * Инициализация кнопок корзины
 */
function initCartButtons() {
    document.querySelectorAll('.btn-cart-add').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            addToCart(this);
        });
    });
}

/**
 * Добавление товара в корзину
 */
function addToCart(button) {
    const productName = button.closest('.card-body')?.querySelector('.card-title')?.textContent || 'Товар';

    const originalText = button.innerHTML;
    const originalClass = button.className;

    // Показываем состояние загрузки
    button.innerHTML = '<span class="loading-spinner me-2"></span>Добавляется...';
    button.classList.remove('btn-success');
    button.classList.add('btn-secondary');
    button.disabled = true;

    // Имитация запроса
    setTimeout(() => {
        // Обновляем счетчик корзины
        updateCartCount(1);

        // Показываем уведомление
        showNotification(`Товар "${productName}" добавлен в корзину!`, 'success');

        // Меняем состояние кнопки
        button.innerHTML = '<i class="fas fa-check me-2"></i>Добавлено';

        // Возвращаем через 2 секунды
        setTimeout(() => {
            button.innerHTML = originalText;
            button.className = originalClass;
            button.disabled = false;
        }, 2000);
    }, 800);
}

/**
 * Обновление счетчика корзины
 */
function updateCartCount(increment) {
    const cartBadge = document.querySelector('.cart-count-badge');
    if (cartBadge) {
        let currentCount = parseInt(cartBadge.textContent) || 0;
        currentCount += increment;
        cartBadge.textContent = currentCount;
    }
}

/**
 * Инициализация алертов (автоскрытие через 5 секунд)
 */
function initAlerts() {
    document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 500);
        }, 5000);
    });
}

/**
 * Показ уведомления
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 4000);
}

/**
 * Простейшая валидация форм (для примера)
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    valid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            if (!valid) {
                e.preventDefault();
                showNotification('Пожалуйста, заполните все обязательные поля', 'danger');
            }
        });
    });
}