from .models import Article
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea

class ArticlesForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'author', 'full_text', 'date']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Article name'
            }),
            "author": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Article author'
            }),
            "date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Publication date'
            }),
            "full_text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Article text'
            })
        }