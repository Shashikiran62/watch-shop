from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from . models import Watches,WatchesUploads,Wishlisst,Cart,WatchReview
from . forms import UploadForm
from . models import CartItem

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login,logout


def home(request):
    watches = WatchesUploads.objects.all()
    context = {'watches_t':watches}
    return render(request, "home.html",context)


def about(request):
    return render(request, "about.html")

@login_required(login_url="/login")
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UploadForm()

    return render(request,"WatchUpload.html",{'form':form})



def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user_name,password=password)
            if user is not None :
                login(request,user)
                return redirect('home')
            else :
                return render(request,"login.html",{'form':form})
    else:
        form = AuthenticationForm()
    return render(request,"login.html",{'form':form})


def signup_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,"signup.html",{'form':form})

def logout_user(request):
    logout(request)
    return redirect('home')


from django.shortcuts import get_object_or_404
def show_product(request,id):
    product = get_object_or_404(WatchesUploads,id=id)
    reviews_obj =  WatchReview.objects.filter(product=product)
    print("This is the object",reviews_obj)
    return render(request,"product.html",{"product":product,"reviews":reviews_obj})

# Wishlist 
from django.contrib import messages
def addtowish(request, id):
    product = get_object_or_404(WatchesUploads, id=id)
    wishlist, created = Wishlisst.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        messages.info(request, "Product is already in your wishlist.")
    else:
        wishlist.products.add(product)
        messages.success(request, "Product added to wishlist successfully!")

    return redirect('home')

@login_required(login_url='/login')
def show_wishlist(request):
    wishlist, created = Wishlisst.objects.get_or_create(user=request.user)
    user_products = wishlist.products.all()
    return render(request, "wishcart.html", {"user_products": user_products})


@login_required(login_url='/login')
def removewish(request, id):
    product = get_object_or_404(WatchesUploads, id=id)
    wishlist, created = Wishlisst.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, "Product removed from wishlist.")
    else:
        messages.warning(request, "Product not found in your wishlist.")

    return redirect('show_wishlist')


# Cart Part
def addtocart(request,id):
    # chcek if user has cart or not
    user_cart,created = Cart.objects.get_or_create(user= request.user)

    # fetch the prodcut with given id
    product = WatchesUploads.objects.get(id=id)

    # create a cart item using the product and user
    cart_item, created= CartItem.objects.get_or_create(user=user_cart,product=product)
    cart_item.product = product
    cart_item.save()
    return redirect('home')


@login_required(login_url='/login')
def show_cartlist(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    # Continue with the rest of the logic
    return render(request, "cartlist.html", {"cart": user_cart})



def removeCart(request,id):
    product_rm = WatchesUploads.objects.get(id=id)
    cart_obj = Cart.objects.get(user=request.user)
    cart_obj.products.remove(product_rm)
    return render(request,"wishcart.html",{"user_products":cart_obj.products.all(),"isCart":True})