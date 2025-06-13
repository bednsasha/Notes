import json
from urllib import request
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from slugify import slugify
from django.contrib.auth.decorators import login_required

from .forms import  noteForm
from .models import   ApplicantProfile, Note, Category

menu=[{'title':'Все заметки','url_name':'home'},
      {'title':'Избранное','url_name':'favourites'},
      {'title':'Корзина','url_name':'basket'},
      {'title':'Папки','url_name':'category'},
      
]


def page_not_found(request,exception):
    return render(request, '404.html', status=404)

@login_required(login_url='/users/login/')
def add_note(request):
    profile = ApplicantProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = noteForm(request.POST, owner=profile)

        if form.is_valid():
            try:
                title = form.cleaned_data['title']
                new_category_name = form.cleaned_data.get('new_category_name')

                if new_category_name != 'Noname' and new_category_name.strip():
                    category, created = Category.objects.get_or_create(
                        name=new_category_name,
                        slug=slugify(new_category_name),
                        owner=profile
                    )
                else:
                    category_id = request.POST.get('category')
                    category = Category.objects.get(id=category_id, owner=profile)

                note = Note.objects.create(
                    title=title if title else 'Noname',
                    slug=slugify(title) if title else slugify('Noname'),
                    content=form.cleaned_data.get('content'),
                    category=category,
                    owner=profile
                )
                return redirect('edit_note', slug=note.slug)
            except Exception as e:
                form.add_error(None, 'Ошибка: ' + str(e))
    else:
        form = noteForm(owner=profile)

    categories = Category.objects.filter(owner=profile)
    data = {
        'form': form,
        'categories': categories,
        'menu': menu,
    }
    return render(request, 'stylenote.html', data)

@login_required(login_url='/users/login/')
def edit_note(request,slug):
    note= Note.objects.get(slug=slug)
    profile = ApplicantProfile.objects.get(user=request.user)
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
                        category, created = Category.objects.get_or_create(name=new_category_name, slug=slugify(new_category_name), owner=profile) 
                form.save()
    categories = Category.objects.filter(owner=profile)
    context = {'form':form, 'create':create,'modify':modify, 'categories': categories, 'menu':menu  }
    return render(request, 'stylenote.html', context)


@login_required(login_url='/users/login/')
def edit_note(request,slug):
    note= Note.objects.get(slug=slug)
    profile = ApplicantProfile.objects.get(user=request.user)
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
                        category, created = Category.objects.get_or_create(name=new_category_name, slug=slugify(new_category_name), owner=profile) 
                        
                     
                form.save()
    categories = Category.objects.filter(owner=profile)
    context = {'form':form, 'create':create,'modify':modify, 'categories': categories, 'menu':menu  }
    return render(request, 'stylenote.html', context)

def categories(request):
    if not request.user.is_authenticated:
        return render(request,'folders.html',{'menu':menu, 'category':None})
    else:
        profile = ApplicantProfile.objects.get(user=request.user)
        return render(request,'folders.html',{'menu':menu, 'category':Category.objects.filter(owner=profile)})


    

def basket(request):
    
    
    if request.user.is_authenticated:
        profile = ApplicantProfile.objects.filter(user=request.user).first()
        if profile:
            list_bask=Note.objects.filter( in_basket=True, owner=profile)
        else:
            list_bask = Note.objects.none()
    else:
       list_bask = Note.objects.none()
   
    return render(request, 'basket.html',{'menu':menu, 'notes':list_bask,})

def favourites(request):
    
    if request.user.is_authenticated:
        profile = ApplicantProfile.objects.filter(user=request.user).first()
        if profile:
            list_favourites=Note.objects.filter(favourites=1, in_basket=False, owner=profile)
        else:
            list_favourites = Note.objects.none()
    else:
       list_favourites = Note.objects.none()
    
    return render(request, 'favourites.html',{'menu':menu, 'notes':list_favourites,})



def certain_categories(request, slug_cat):
    profile = ApplicantProfile.objects.get(user=request.user)
    cat_id= get_object_or_404(Category, slug=slug_cat, owner=profile)
    notes=Note.objects.filter(category_id=cat_id.id,  in_basket=False, owner=profile)
    return render(request, 'folder_note.html', {'menu':menu,'slug':slug_cat, 'notes':notes})

class CategoryEditView(LoginRequiredMixin, View):
    def post(self, request, pk):
        profile = ApplicantProfile.objects.get(user=request.user)
        cat = get_object_or_404(Category, pk=pk, owner=profile)
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
    if request.user.is_authenticated:
        profile = ApplicantProfile.objects.filter(user=request.user).first()
        if profile:
            notes = Note.objects.filter(in_basket=False, owner=profile)
        else:
            notes = Note.objects.none()
    else:
        notes = Note.objects.none()

    return render(request, 'main.html', {'menu': menu, 'notes': notes})


@login_required(login_url='/users/login/')
def list_fav(request, note_id):
    profile = ApplicantProfile.objects.get(user=request.user)
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=note_id, owner=profile)
        note.favourites = not note.favourites # Переключаем состояние
        note.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required(login_url='/users/login/')
def list_basket(request, note_id):
    if request.method == 'POST':
        profile = ApplicantProfile.objects.get(user=request.user)
        note = get_object_or_404(Note, pk=note_id, owner=profile)
        note.in_basket = not note.in_basket  # Переключаем состояние
        print(f"Note ID: {note.id}, in_basket: {note.in_basket}")  # Для отладки
        note.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))
    #return JsonResponse({"success": True}) 

@login_required(login_url='/users/login/')
def delete_note(request, note_id):
    if request.method == 'POST':
        profile = ApplicantProfile.objects.get(user=request.user)
        note = get_object_or_404(Note, pk=note_id, owner=profile)
        note.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required(login_url='/users/login/')
def add_folder(request):
    if request.method == "POST":
        name = request.POST.get('name', 'Noname').strip()
        if not name:
            name = 'Noname'
        try:
            profile = ApplicantProfile.objects.get(user=request.user)
        except ApplicantProfile.DoesNotExist:
            return JsonResponse({'error': 'Профиль пользователя не найден'}, status=400)

        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        # Избегаем конфликта slug в рамках одного владельца
        while Category.objects.filter(slug=slug, owner=profile).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        category = Category.objects.create(name=name, slug=slug, owner=profile)
        return JsonResponse({'message': 'Категория создана', 'id': category.id, 'name': category.name})
    else:
        return JsonResponse({'error': 'Неверный метод'}, status=405)
    

        