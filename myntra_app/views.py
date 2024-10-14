import stripe
import json
from django.shortcuts import render,redirect
from .models import Product
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'

# def payment_handler(request):
#    print("Hello")
#    if request.method=='POST':
#       print(request.POST['checkout-button'])
#       return redirect('/')

@csrf_exempt
def create_checkout_session(request):
    if request.method=='POST':
        amt=json.load(request)['post_data']
        session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
        'price_data': {
        'currency': 'inr',
        'product_data': {
        'name': 'Your Order',
        },
        'unit_amount': amt*100,
        },
        'quantity': 1,
        }],
        mode='payment',

        success_url=YOUR_DOMAIN + '/success',
        cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return JsonResponse({'id': session.id})
    return redirect('/')

def success(request):
   return render(request,'myntra_app/success.html')

def cancel(request):
   return render(request,'myntra_app/cancel.html')

def home(request):
    my_product=Product.objects.all()
    context={
        "myproduct":my_product
    }
    return render(request,'myntra_app/index.html',context)

def mycart(request):
    return render(request,'myntra_app/mycart.html')

