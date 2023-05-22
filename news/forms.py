from .models import News
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['title', 'anons', 'full_text', 'date']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'News article name'
            }),
            "anons": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'News article anons'
            }),
            "date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Publication date'
            }),
            "full_text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'News article text'
            })
        }