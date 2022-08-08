import json
from pyexpat.errors import messages

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.http import HttpResponse

from bidding_app.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# relative import of forms
from .models import AddProduct, BidProduct
from .forms import AddProductForm



def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        mobile_number = request.POST.get('mobile_number')

        if User.objects.filter(mobile_number=mobile_number).exists():
            messages.info(request, 'Mobile number taken')
            return redirect('/signup')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'EMAIL taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, mobile_number=mobile_number)
                user.save()
                print("User created")
                return redirect('/')
        else:
            messages.info(request, 'password not matching...')
            return redirect('/signup')
    else:
        return render(request, 'bidding_app/registration.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print(request.user)
            request.session['username'] = username
            request.session.set_expiry(300)
            return redirect('/home')
        else:
            return render(request, 'bidding_app/login.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'bidding_app/login.html')


@login_required(login_url='/')
def logout_user(request):
    logout(request)
    print(request.user)
    return redirect('/')


@login_required(login_url='/')
def home(request):
    prod_obj = AddProduct.objects.all()
    context = {
        'prod_obj': prod_obj
    }
    return render(request, 'bidding_app/home.html', context)


def create_view(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    form = AddProductForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            prod_form = form.save(commit=False)
            prod_form.user = request.user
            prod_form.save()
            return  redirect('home')

    context['form'] = form
    return render(request, "bidding_app/create_view.html", context)


def prod_detail(request, key):
    prod_obj = AddProduct.objects.get(id=key)
    admin_bid_obj = BidProduct.objects.filter(product=prod_obj)
    bid_obj = None
    if request.user.is_authenticated and BidProduct.objects.filter(product=prod_obj, user=request.user).exists():
        bid_obj = BidProduct.objects.get(product=prod_obj, user=request.user)

    context = {
        'prod_obj': prod_obj,
        'bid_obj': bid_obj,
        'admin_bid_obj': admin_bid_obj
    }
    return render(request, "bidding_app/detail_view.html", context)

@csrf_exempt
def create_bid(request):
    if request.is_ajax():

        bid_amount = request.POST.get('amount')
        prod = request.POST.get('prod')

        if BidProduct.objects.filter(user = request.user,product = AddProduct.objects.get(id=prod)).exists():
            BidProduct.objects.get(user=request.user, product=AddProduct.objects.get(id=prod)).delete()
        BidProduct.objects.create(
            user = request.user,
            product = AddProduct.objects.get(id=prod),
            bid_amount = bid_amount
        )
        response = {
            'success': True,
        }
        return JsonResponse(response)

@csrf_exempt
def bid_filter(request):
    if request.is_ajax():
        select_type = request.POST.get('select_type')
        admin_bid_obj = BidProduct.objects.all()
        if select_type == 'low':
            admin_bid_obj = admin_bid_obj.order_by('bid_amount')
        if select_type == 'high':
            admin_bid_obj = admin_bid_obj.order_by('-bid_amount')
        context = {
            'admin_bid_obj': admin_bid_obj
        }
        data = render_to_string(
            'bidding_app/bid_table.html', context, request=request)
        response = {
            'success': True,
            'data': data,
        }
        return HttpResponse(json.dumps(response))

def delete_bid(request, key):
    AddProduct.objects.get(id=key).delete()
    return redirect('home')