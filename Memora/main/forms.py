from django import forms

from .models import Category, Note



class noteForm(forms.ModelForm):
    new_category_name = forms.CharField(required=False, empty_value='Noname', widget=forms.Textarea(attrs={'class': 'w-100', 'rows':1}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':"input-textarea mt-4",  'placeholder':"О чем вы думаете? Запишите свои мысли..."}), required=False)
    title = forms.CharField(widget=forms.Textarea(attrs={'class': 'title-note', 'placeholder': 'Заголовок', 'rows': 1}), required=False, initial='Noname')
    favourites = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Note
        fields = ['title', 'content', 'favourites', 'category']

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)
        if owner:
            self.fields['category'].queryset = Category.objects.filter(owner=owner)
