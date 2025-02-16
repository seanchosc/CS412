from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.conf.urls.static import static
# Create your views here.

images = [
    'images/restaurant/logo.png',
    'images/restaurant/storefront.png',
]

def main(request):
    '''Show the main page.'''
    template_name = "restaurant/main.html" # Main template from templates folder
    logo = images[0] # Refers to first image (logo) in the list
    storefront = images[1] # Refers to second (storefront)
    context = {
        'logo' : logo, # Context variable for logo
        'storefront' : storefront, # Context variable for storefront
    }
    return render(request, template_name, context)

def order(request):
    '''Show the web page with the form.'''
    template_name = "restaurant/order.html" # Order template from templates folder
    return render(request, template_name)

def confirmation(request):
    '''Show the order confirmation.'''
    template_name = "restaurant/confirmation.html" # Confirmation template from templates folder
    return render(request, template_name)


