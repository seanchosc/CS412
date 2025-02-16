from django.shortcuts import render
# Create your views here.
def main(request):
    '''Show the main page.'''
    template_name = "restaurant/main.html" # Main template from templates folder
    return render(request, template_name)

def order(request):
    '''Show the web page with the form.'''
    template_name = "restaurant/order.html" # Order template from templates folder
    return render(request, template_name)

def confirmation(request):
    '''Show the order confirmation.'''
    template_name = "restaurant/confirmation.html" # Confirmation template from templates folder
    return render(request, template_name)


