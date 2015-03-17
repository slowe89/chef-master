

from django.conf import settings
from base_app.CustomForm import CustomForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django_mako_plus.controller import view_function
from django.contrib.auth.decorators import permission_required
import base_app.models as hmod
from django.utils.translation import ugettext as _
from django_mako_plus.controller.router import get_renderer
from django.utils import timezone

templater = get_renderer('inventory')

@view_function
#@permission_required(['base_app.change_wardrobeitem', 'base_app.change_nonwardrobeitem'], login_url='/homepage/login/')
def process_request(request):

    # Define the view bag
    params = {}

    inventory = hmod.Inventory.objects.all()
    products = hmod.SerializedProduct.objects.all()

    params['inventory'] = inventory

    return templater.render_to_response(request, 'products.html', params)

@view_function
#@permission_required(['base_app.change_wardrobeitem', 'base_app.change_nonwardrobeitem'], login_url='/homepage/login/')
def details(request):

    # Define the view bag
    params = {}

    try:
        thisProduct = hmod.Inventory.objects.get(id=request.urlparams[0])
    except hmod.Inventory.DoesNotExist:
        return HttpResponseRedirect('/inventory/products/')

    params['product'] = thisProduct

    return templater.render_to_response(request, 'productDetails.html', params)


@view_function
#@permission_required(['base_app.change_wardrobeitem', 'base_app.change_nonwardrobeitem'], login_url='/homepage/login/')
def find(request):

    # Define the view bag
    params = {}

    if request.REQUEST.get('name'):
        try:
            product = hmod.Inventory.objects.get(name=request.REQUEST.get('name'))
            return HttpResponse('/inventory/products.details/' + str(product.id))
        except hmod.Inventory.DoesNotExist:
            print('Product not found')

    return templater.render_to_response(request, 'find.html', params)

@view_function
def report(request):

    # Define the view bag
    params={}

    # Grab the items that are overdue
    items = hmod.RentalItem.objects.filter(due_date__range=['1900-01-01',timezone.now()], date_in=None)

    params['items'] = items
    params['report_name'] = 'Overdue Rental Items'

    print(items[0].transaction.customer.get_full_name())

    return templater.render_to_response(request, 'report.html', params)

#changes go here