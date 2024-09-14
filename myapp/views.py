from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from .functions import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
import logging
from django.template import loader
import uuid, random
import time
from .models import *
from django.utils import timezone
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg = 'User created successfully.'
            success = True
            # return redirect("/login/")
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



@login_required(login_url="/login/")
def index(request):
    random_number = random.randint(1530, 6000)
    random_number1 = random.randint(7910, 87020)
    random_number2 = random.randint(1367, 7700)
    context = {'segment': 'index', 'random_number': random_number,'random_number1': random_number1, 'random_number2': random_number2}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


# coins page
@login_required(login_url="/login/")
def tiktokcoins(request):
    coin_options = CoinOption.objects.all()
    context = {
        'segment': 'tiktokcoins',
        'coin_options': coin_options,
    }
    return render(request, 'home/tiktokcoins.html', context)


# tiktok id data
@login_required(login_url="/login/")
@csrf_exempt
def gettiktokiddata(request):
    if request.method == 'POST':
        tiktokid = request.POST['tiktokid']
        print(f"Received TikTok ID: {tiktokid}")
        data = fetch_tiktok_data(tiktokid)
        print(data)
        return JsonResponse({'message': 'Success', 'tiktokid': data})
    return JsonResponse({'message': 'Invalid request'}, status=400)


# invoice tiktok
@csrf_exempt
@login_required(login_url="/login/")
def tiktokinvoice(request):
    if request.method == 'POST':
        tiktok_id = request.POST.get('tiktokid')
        coin = request.POST.get('coin')
        price = request.POST.get('price')
        coin = coin.replace('Coins', '').strip()
        price = price.replace('Price: ', '').strip()
        print("==============", coin, price, tiktok_id)
        generator = UniqueIDGenerator()
        invoice_id = generator.generate_unique_id()
        data = fetch_tiktok_data(tiktok_id)
        coin_details = {
            'coin': coin,
            'price': price,
            'tiktok_id': tiktok_id,
            'invoice_id': invoice_id,
            'data': data,
        }
        context = {'coin': coin_details}
        return render(request, "home/tiktokinvoice.html", context)
    # return render(request, "home/tiktokinvoice.html")



# sucesscoins
@csrf_exempt
@login_required(login_url="/login/")
def sucesscoins(request):
    if request.method == 'POST':
        invoice_id = request.POST.get('invoice_id')
        username = request.POST.get('username')
        print(username)
        coin = request.POST.get('coin')
        price = request.POST.get('price')
        data = fetch_tiktok_data(username)
        print(data)
        print("coins ==============>",  username, coin, price, invoice_id)
        # Create and save the Invoice instance
        profile = TikTokProfiledata(
            item=f'{coin} Coins',
            price=int(price),
            date= timezone.now().date(),
            invoice_id= invoice_id,
            profile_name=data['profile_name'],
            username=data['username'],
            followers=data['followers'],
            likes=data['likes'],
            following=data['following'],
            signature=data['signature'],
            biolink=data['biolink'],
            video_count=data['video_count'],
            unique_id=data['unique_id'],
            nickname=data['nickname'],
            avatar_url=data['avatar_url'],
            # status=profile_data.get('status', 'Processing'),
            # comments=profile_data.get('comments', 'This should take a while'),
            # issue=profile_data.get('issue', 'Carding coins')
        )
        profile.save()
        # Access the ID of the newly saved profile
        # profile_id = profile.id
        # print(f'The ID of the newly saved profile is: {profile_id}')

        coin_details = {
            'coin': coin,
            'price': price,
            'invoice_id': invoice_id,
            'username': username,
        }
        context = {'data': coin_details}
        return JsonResponse({'message': 'Success'})    


#  diamonds page
@login_required(login_url="/login/")
def Likeediamonds(request):
    c_options = diamondsOption.objects.all()
    context = {
        'segment': 'Likeediamonds',
        'c_options': c_options,
                       }
    return render(request, 'home/Likeediamonds.html', context)


#  Likee id data
@csrf_exempt
@login_required(login_url="/login/")
def getlikeeiddata(request):
    if request.method == 'POST':
        tiktokid = request.POST['tiktokid']
        print(f"Received Likee ID: {tiktokid}")
        data = likee_profile_info(tiktokid)
        print(data)
        return JsonResponse({'message': 'Success', 'tiktokid': data})
    return JsonResponse({'message': 'Invalid request'}, status=400)



# likee invoice
@csrf_exempt
@login_required(login_url="/login/")
def likeeinvoice(request):
    if request.method == 'POST':
        tiktok_id = request.POST.get('tiktokid')
        coin = request.POST.get('coin')
        price = request.POST.get('price')
        coin = coin.replace('Diamonds', '').strip()
        price = price.replace('Price: ', '').strip()
        print("==============", coin, price, tiktok_id)
        generator = UniqueIDGenerator()
        invoice_id = generator.generate_unique_id()
        data = likee_profile_info(tiktok_id)

        coin_details = {
            'coin': coin,
            'price': price,
            'tiktok_id': tiktok_id,
            'invoice_id': invoice_id,
            'data': data,
        }
        context = {'coin': coin_details}
        return render(request, "home/likeeinvoice.html", context)
    # return render(request, "home/likeeinvoice.html")


# sucessdiamonds
@csrf_exempt
@login_required(login_url="/login/")
def sucessdiamonds(request):
    if request.method == 'POST':
        invoice_id = request.POST.get('invoice_id')
        username = request.POST.get('username')
        diamonds = request.POST.get('coin')
        price = request.POST.get('price')
        print("diamonds ==============>", diamonds, price, invoice_id, username)
        data = likee_profile_info(username)
        # Create and save the Invoice instance
        profile = LikeeProfiledata(
            item=f'{diamonds} Diamonds',
            price=int(price),
            date= timezone.now().date(),
            invoice_id= invoice_id,
            profile_name=data['Profile_Name'],
            username=data['Username'],
            followers=data['Followers'],
            likes=data['Likes'],
            bio=data['Bio'],
            avatar_url=data['Image_URL'],
        )
        profile.save()

        coin_details = {
            'diamonds': diamonds,
            'price': price,
            'invoice_id': invoice_id,
            'username': username,
        }
        context = {'data': coin_details}
        return JsonResponse({'message': 'Success'})



# status tracking
def tracking(request):
    tiktoktracking = TikTokProfiledata.objects.all()
    likeetracking = LikeeProfiledata.objects.all()
    context = {
        'segment': 'tracking',
        'tiktoktracking': tiktoktracking,
        'likeetracking': likeetracking,
            }
    # print(context)
    return render(request, 'home/status.html', context)

    