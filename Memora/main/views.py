import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from slugify import slugify


from .forms import  noteForm
from .models import   Note, Category

menu=[{'title':'Все заметки','url_name':'home'},
      {'title':'Избранное','url_name':'favourites'},
      {'title':'Корзина','url_name':'basket'},
      {'title':'Папки','url_name':'category'},
      
]

def page_not_found(request,exception):
    return render(request, '404.html', status=404)



def add_note (request):
    
    if request.method=='POST':
            form = noteForm(request.POST)
            
            if form.is_valid():
                try:
                    title = form.cleaned_data['title']
                    
                    new_category_name = form.cleaned_data.get('new_category_name')
                    if new_category_name:
                        category, created = Category.objects.get_or_create(name=new_category_name, slug=slugify(new_category_name))
                    note = Note.objects.create(
                    title=title,
                    slug = slugify(title),
                    content=form.cleaned_data.get('content'),
                    category_id=category.pk
                    ) 
                    
                    return redirect('edit_note', slug=note.slug)
                    
                except Exception as e:
                    form.add_error(None, 'Ошибка: ' + str(e))
                    print(slugify(form.cleaned_data['title']))
                    
                
    else:
        form = noteForm()
    categories = Category.objects.all()  # Получаем все категории
    data = {
        'form': form,
        'categories': categories, # Передаем категории в контекст
        'menu': menu,
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
                new_category_name = form.cleaned_data.get('new_category_name')
                if note.slug!=slugify((form.cleaned_data['title'])):
                    note.slug =slugify((form.cleaned_data['title']))
                    note.title = form.cleaned_data['title']  
                    note.save() 
                    return redirect('edit_note', slug=note.slug)
                    
                if new_category_name:
                        category, created = Category.objects.get_or_create(name=new_category_name, slug=slugify(new_category_name)) 
                        
                     
                form.save()
    categories = Category.objects.all()
    context = {'form':form, 'create':create,'modify':modify, 'categories': categories, 'menu':menu  }
    return render(request, 'note.html', context)

def categories(request):
    return render(request,'folders.html',{'menu':menu, 'category':Category.objects.all()})


    

def basket(request):
    list_bask=Note.objects.filter( in_basket=True)
    return render(request, 'basket.html',{'menu':menu, 'notes':list_bask,})

def favourites(request):
    list_favourites=Note.objects.filter(favourites=1, in_basket=False)
    return render(request, 'favourites.html',{'menu':menu, 'notes':list_favourites,})

def authorization(request):
    return render(request, 'authorization.html')

def registration(request):
    return render(request, 'registration.html')

def password_change(request):
    return render(request, 'password_change.html')

def code(request):
    return render(request, 'code.html')

def certain_categories(request, slug_cat):
    cat_id= get_object_or_404(Category, slug=slug_cat)
    notes=Note.objects.filter(category_id=cat_id.id,  in_basket=False)
    return render(request, 'folder_note.html', {'menu':menu,'slug':slug_cat, 'notes':notes})

class CategoryEditView(View):
    def post(self, request, pk):
        cat = get_object_or_404(Category, pk=pk)
        data = json.loads(request.body)
        new_name = data.get('name', '').strip()
        if new_name:
            cat.name = new_name
            if cat.slug!=slugify(cat.name):
                cat.slug=slugify(cat.name)
            cat.save()
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error'}, status=400)

def main(request):
    notes=Note.objects.filter(in_basket=False)
    return render(request,'main.html',{'menu':menu,'notes':notes})

def list_fav(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=note_id)
        note.favourites = not note.favourites # Переключаем состояние
        note.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def list_basket(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=note_id)
        note.in_basket = not note.in_basket  # Переключаем состояние
        print(f"Note ID: {note.id}, in_basket: {note.in_basket}")  # Для отладки
        note.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))
    #return JsonResponse({"success": True}) 

def delete_note(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=note_id)
        note.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def Add_note(request):
    if request.method == 'POST':
        form = noteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            new_cat_name = form.cleaned_data.get('new_category_name')
            if new_cat_name:
                # Создаем новую категорию (пример, если у вас есть модель Category)
                category = Category.objects.create(name=new_cat_name)
                note.category = category
            else:
                # Используем выбранную категорию из формы
                note.category = form.cleaned_data.get('category')
            note.save()
            return redirect('some_view_name', note.pk)
    else:
        form = noteForm()
    return render(request, 'note(style).html', {'form': form})


def Edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = noteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            return redirect('note(style).html', note.pk)  # Перенаправление на подробности заметки
    else:
        form = noteForm(instance=note)
    
    return render(request, 'note(style).html', {'form': form})

def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'note(style).html', {'note': note})