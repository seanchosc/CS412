from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.conf.urls.static import static
import random
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
        'logo' : logo, # Context variable for logo photo
        'storefront' : storefront, # Context variable for storefront photo
    }
    return render(request, template_name, context)

def order(request):
    '''Show the web page with the form.'''
    template_name = "restaurant/order.html" # Order template from templates folder
    specials = [
        'BBQ Chicken Pizza - $14',
        'Buffalo Wings - $14',
        'Pork Tacos - $14',
    ]
    special = random.choice(specials)
    return render(request, template_name, {'special': special})

## restaurant/views.py: submit function
def submit(request):
    '''Process the form submission, and generate a result.'''
    template_name = "restaurant/confirmation.html"
    if request.POST:

        name = request.POST['name']
        number = request.POST['number']
        email = request.POST['email']

        order = []
        total = 0
        if 'special' in request.POST:
            order.append("Daily Special")
            total += 14
        if 'pepperoni' in request.POST:
            order.append("Pepperoni Pizza")
            total += 12
        if 'cheese' in request.POST:
            order.append("Cheese Pizza")
            total += 10
        if 'hotdog' in request.POST:
            order.append("Hotdog")
            total += 6
        if 'instructions' in request.POST:
            instructions = request.POST['instructions']
        else:
            instructions = "None"
        if 'shake' in request.POST:
            order.append("Shake")
            total += 5
            selectedflavor = request.POST.get('flavor', '')
            if selectedflavor == '':
                flavor = "Not specified, will choose at random"
            else:
                flavor = selectedflavor
        else:
            flavor = "No shake ordered"
        context = {
            'name': name, # Name context variable
            'number': number, # Phone number context variable
            'email': email, # email
            'order': order if order else ['No order'], # context variable for items
            'flavor' : flavor, # context variable for shake flavor
            'instructions': instructions, # context variable for instructions
            'total' : total # total context variable
        }
        request.session['confirmation'] = context
    return render(request, template_name, context=context)

def confirmation(request):
    '''Show the order confirmation.'''
    template_name = "restaurant/confirmation.html" # Confirmation template from templates folder
    return render(request, template_name)


