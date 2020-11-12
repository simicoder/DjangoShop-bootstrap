from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from store.models import *
from django.db.models import Q
from chat.models import Room


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user.is_active = True
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


def home_view(request, query=None, category=None):
    if category is None:
        queryset = Product.objects.all()
    else:
        category = get_object_or_404(Category, name=category)
        queryset = Product.objects.filter(category=category)

    categories = Category.objects.all()

    query = ""

    if request.GET:
        queryset = []
        query = request.GET['q']

        queries = query.split(" ")
        for q in queries:
            products = Product.objects.filter(Q(title__icontains=q)).distinct()

            for prod in products:
                queryset.append(prod)
    
        queryset = list(set(queryset))

    context = {
        'products': queryset,
        'categories': categories,
    }

    return render(request, 'store/home.html', context)

@login_required
def create_view(request):
    image_form_set = modelformset_factory(ProductImage, form=ProductImageForm, extra=6)

    if request.method == 'POST':
        form = ProductForm(request.POST or None)
        formset = image_form_set(request.POST, request.FILES, queryset=ProductImage.objects.none())
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            for form in formset.cleaned_data:
                if form:
                    image = form['img']
                    photo = ProductImage(product=product, img=image)
                    photo.save()
                else:
                    continue
            return HttpResponseRedirect("/")
    else:
        form = ProductForm()
        formset = image_form_set(queryset=ProductImage.objects.none())

    context = {
        'form': form,
        'img_form': formset
    }
    return render(request, 'store/createProduct.html', context)


def info_view(request):
    return render(request, 'store/info.html')


def product_view(request, id):
    product = get_object_or_404(Product, id=id)

    img_slides = product.images.all()

    if request.POST.get("delete"):
        product.delete()
        return redirect("/")

    if request.POST.get("chat"):
        if Room.objects.filter(user_1=request.user, user_2=product.seller) or Room.objects.filter(user_1=product.seller, user_2=request.user):
            return redirect("/chat/"+request.user.username+product.seller.username)
        else:
            chat = Room(room_name=request.user.username+product.seller.username, user_1=request.user, user_2=product.seller)
            chat.save()
            return redirect("/chat/"+request.user.username+product.seller.username)

    context = {
        'user': request.user,
        'product': product,
        'img_slides': img_slides,
    }
    return render(request, 'store/product_view.html', context)

@login_required
def account_info_view(request):
    queryset = Product.objects.filter(seller=request.user)

    if request.POST.get("delete"):
        queryset.delete()

    context = {
        'products': queryset
    }
    return render(request, 'store/account.html', context)
