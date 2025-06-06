from django import forms

from .models import Note, Category




class noteForm(forms.ModelForm):
    new_category_name = forms.CharField(required=False)  # Поле для создания новой категории
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5,'class':'form-control',  'placeholder':'Start writing...'}), required=False)
    class Meta:
        model = Note
        fields = ['title', 'content', 'favourites', 'category']  # Для использования уже существующей категории
        