from django import forms

from .models import Category, Note


   
class noteForm(forms.ModelForm):
      class Meta:
          model = Note
          #form fields/inputs that will be shown
          fields = ['title', 'content']
          #added a css class and html placeholder to the form inputs
          #the form-control css class is from bootstrap
          widgets={
                  'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Note title'}),
                  'content':forms.Textarea(attrs={'class':'form-control',  'placeholder':'Start writing...'}),
                  'category' : forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
          }