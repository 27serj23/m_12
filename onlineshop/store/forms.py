from django import forms
from .models import Contact, Review


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'author_name', 'email', 'text', 'rating']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com (необязательно)'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш отзыв'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'placeholder': 'Оценка 1-5'}),
        }
        labels = {
            'product': 'Выберите товар',
            'author_name': 'Имя',
            'email': 'Email',
            'text': 'Отзыв',
            'rating': 'Оценка',
        }