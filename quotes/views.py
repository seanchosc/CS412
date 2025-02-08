from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
# Create your views here.
quotes = [
    "We can't solve problems by using the same kind of thinking we used when we created them.",
    "Try not to become a man of success. Rather, become a man of value.",
    "Anyone who has never made a mistake has never tried anything new."
    ]   

images = [
    'images/einstein1.png',
    'images/einstein2.png',
    'images/einstein3.png',
    ]
def base(request):
    '''Define a view to show the 'base.html' template.'''

    # the template to which we will delegate the work
    template = 'hw/base.html'

    # a dict of key/value pairs, to be available for use in template
    quote = random.choice(quotes)
    image = random.choice(images)
    context = {
        'quote': quote,
        'image': image
    }
    return render(request, template, context)
def quote(request):
    '''Define a view to show the 'quote.html' template.'''

    # the template to which we will delegate the work
    template = 'hw/quote.html'

    # a dict of key/value pairs, to be available for use in template
    quote = random.choice(quotes)
    image = random.choice(images)
    context = {
        'quote': quote,
        'image': image
    }
    return render(request, template, context)

def show_all(request):
    '''Define a view to show the 'show_all.html' template.'''

    # the template to which we will delegate the work
    template = 'hw/show_all.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        "quote1": quotes[0],
        "quote2": quotes[1],
        "quote3": quotes[2],
        "image1": images[0],
        "image2": images[1],
        "image3": images[2],
    }
    return render(request, template, context)

def about(request):
    '''Define a view to show the 'about.html' template.'''

    # the template to which we will delegate the work
    template = 'hw/about.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
    }
    return render(request, template, context)
    