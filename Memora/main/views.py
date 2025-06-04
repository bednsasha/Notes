from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.text import slugify

from .forms import noteForm
from .models import Category, Note

def page_not_found(request,exception):
    return render(request, '404.html', status=404)

def index(request):
    notes=Note.objects.all()
    return render (request, 'index.html', {'notes':notes})

def add_note (request):
    
    if request.method=='POST':
            form = noteForm(request.POST)
            if form.is_valid():
                try:
                    title = form.cleaned_data['title']
                    note = Note.objects.create(
                    title=title,
                    slug=slugify(title),  
                    content=form.cleaned_data.get('content')  
                    )
                    return redirect('edit_note', slug=slugify(title))
                    
                except:
                    form.add_error(None,'Ошибка')
                    
                
    else:
        form = noteForm()
    data={
        'form':form,
        'title':'Noname note'
    }
    return render(request, 'note.html', data)

def edit_note(request,slug):
    note= Note.objects.get(slug=slug)
    
    form = noteForm(instance=note)
    create=note.created_at 
    modify=note.modified_at
    
    if request.method == 'POST':
            form = noteForm(request.POST, instance=note)
            if form.is_valid():
                  form.save()
        
    context = {'form':form, 'create':create,'modify':modify}
    return render(request, 'note.html', context)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Note.published.filter(cat_id=category.pk).select_related("cat")

    data = {
        'title': f'Категория: {category.name}',
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'index.html', context=data) 
    



def authorization(request):
    return render(request, 'authorization.html')

def registration(request):
    return render(request, 'registration.html')

def password_change(request):
    return render(request, 'password_change.html')

def code(request):
    return render(request, 'code.html')