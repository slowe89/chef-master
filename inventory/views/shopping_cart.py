from django.conf import settings
from base_app.CustomForm import CustomForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django_mako_plus.controller import view_function
from django.contrib.auth.decorators import permission_required, login_required
import base_app.models as hmod
from django.utils.translation import ugettext as _
from django_mako_plus.controller.router import get_renderer
from django.utils import timezone
from base_app.CustomWidgets import CustomSelect, CustomRadioRenderer


##########################################################################################
###################################### DEFAULT ACTION ####################################
##########################################################################################

templater = get_renderer('inventory')

@view_function
#@permission_required(['base_app.change_wardrobeitem', 'base_app.change_nonwardrobeitem'], login_url='/homepage/login/')
def process_request(request):
    params = {}
    items = {}

    #get the items to load in the shopping cart modal
    if 'shopping_cart' in request.session:
        for id in request.session['shopping_cart']:

            try:
                cart_item = hmod.Inventory.objects.get(id=id)
            except hmod.Inventory.DoesNotExist:
                HttpResponse('nothing here')

            items[cart_item] = request.session['shopping_cart'][id]
    else:
        request.session['shopping_cart'] = {}

    totalPrice = 0
    params['items'] = items
    params['totalPrice'] = totalPrice

    return templater.render_to_response(request, 'shoppingCart.html', params)

@view_function
def add(request):

    # Define the view bag
    params = {}

    id = request.urlparams[0]
    qty = int(request.urlparams[1])

    if 'shopping_cart' not in request.session:
        request.session['shopping_cart'] = {}
    if id not in request.session['shopping_cart']:
        request.session['shopping_cart'][id] = qty
    else:
        request.session['shopping_cart'][id] += qty

    request.session.modified = True

    return HttpResponseRedirect('/inventory/shopping_cart')

@view_function
def delete(request):

    # Define the view bag
    params = {}

    id = request.urlparams[0]

    del request.session['shopping_cart'][id]

    request.session.modified = True

    return HttpResponseRedirect('/inventory/shopping_cart')


@view_function
@login_required(login_url="/homepage/login.required")
def checkOut(request):

    # Define the view bag
    params = {}

    try:
        user = hmod.User.objects.get(id=request.user.id)
    except hmod.User.DoesNotExist:
        return HttpResponseRedirect('/homepage/index/')

    # Pass in user data to the form
    form = checkoutForm(request, initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'address1': user.address1,
        'address2': user.address2,
        'city': user.city,
        'state': user.state,
        'ZIP': user.ZIP,
        })

    params['form'] = form

    return templater.render_to_response(request, 'checkOut.html', params)

@view_function
def payment(request):

    # Define the view bag
    params = {}

    return templater.render_to_response(request, 'payment.html', params)

@view_function
def success(request):

    # Define the view bag
    params = {}

    return templater.render_to_response(request, 'success.html', params)

class checkoutForm(CustomForm):

    ''' Class for the form to be used in editing the users. '''

    # List of constants for the states:
    ALASKA = 'AK'
    ALABAMA = 'AL'
    ARKANSAS = 'AR'
    ARIZON = 'AZ'
    CALIFORNIA = 'CA'
    COLORADO = 'CO'
    CONNECTICUT = 'CT'
    DELAWARE = 'DE'
    FLORIDA = 'FL'
    GEORGIA = 'GA'
    HAWAII = 'HI'
    IOWA = 'IA'
    IDAHO = 'ID'
    ILLINOIS = 'IL'
    INDIANA = 'IN'
    KANSAS = 'KS'
    LOUISIANA = 'LA'
    MASSACHUSETTS = 'MA'
    MARYLAND = 'MD'
    MAINE = 'ME'
    MICHIGAN = 'MI'
    MINNESOTA = 'MN'
    MISSOURI = 'MO'
    MISSISSIPPI = 'MS'
    MONTANA = 'MT'
    NORTH_CAROLINA = 'NC'
    NORTH_DAKOTA = 'ND'
    NEBRASKA = 'NE'
    NEW_HAMPSHIRE = 'NH'
    NEW_JERSEY = 'NJ'
    NEW_MEXICO = 'NM'
    NEVADA = 'NV'
    NEW_YORK = 'NY'
    OHIO = 'OH'
    OKLAHOMA = 'OK'
    OREGON = 'OR'
    PENNSYLVANIA = 'PA'
    RHODE_ISLAND = 'RI'
    SOUTH_CAROLINA = 'SC'
    SOUTH_DAKOTA = 'SD'
    TENNESSEE = 'TN'
    TEXAS = 'TX'
    UTAH = 'UT'
    VIRGINIA = 'VA'
    VERMONT = 'VT'
    WASHINGTON = 'WA'
    WISCONSIN = 'WI'
    WEST_VIRGINIA = 'WV'
    WYOMING = 'WY'

    # Choices list of tuples for the car_states field
    STATE_CHOICES = (
        (ALASKA, 'Alaska'),
        (ALABAMA, 'Alabama'),
        (ARKANSAS, 'Arkansas'),
        (ARIZON, 'Arizon'),
        (CALIFORNIA, 'California'),
        (COLORADO, 'Colorado'),
        (CONNECTICUT, 'Connecticut'),
        (DELAWARE, 'Delaware'),
        (FLORIDA, 'Florida'),
        (GEORGIA, 'Georgia'),
        (HAWAII, 'Hawaii'),
        (IOWA, 'Iowa'),
        (IDAHO, 'Idaho'),
        (ILLINOIS, 'Illinois'),
        (INDIANA, 'Indiana'),
        (KANSAS, 'Kansas'),
        (LOUISIANA, 'Louisiana'),
        (MASSACHUSETTS, 'Massachusetts'),
        (MARYLAND, 'Maryland'),
        (MAINE, 'Maine'),
        (MICHIGAN, 'Michigan'),
        (MINNESOTA, 'Minnesota'),
        (MISSOURI, 'Missouri'),
        (MISSISSIPPI, 'Mississippi'),
        (MONTANA, 'Montana'),
        (NORTH_CAROLINA, 'North Carolina'),
        (NORTH_DAKOTA, 'North Dakota'),
        (NEBRASKA, 'Nebraska'),
        (NEW_HAMPSHIRE, 'New Hampshire'),
        (NEW_JERSEY, 'New Jersey'),
        (NEW_MEXICO, 'New Mexico'),
        (NEVADA, 'Nevada'),
        (NEW_YORK, 'New York'),
        (OHIO, 'Ohio'),
        (OKLAHOMA, 'Oklahoma'),
        (OREGON, 'Oregon'),
        (PENNSYLVANIA, 'Pennsylvania'),
        (RHODE_ISLAND, 'Rhode Island'),
        (SOUTH_CAROLINA, 'South Carolina'),
        (SOUTH_DAKOTA, 'South Dakota'),
        (TENNESSEE, 'Tennessee'),
        (TEXAS, 'Texas'),
        (UTAH, 'Utah'),
        (VIRGINIA, 'Virginia'),
        (VERMONT, 'Vermont'),
        (WASHINGTON, 'Washington'),
        (WISCONSIN, 'Wisconsin'),
        (WEST_VIRGINIA, 'West Virginia'),
        (WYOMING, 'Wyoming'),
    )

    ## Class title ##
    title = "Shipping Information"
    link = "homepage/index"
    delete_button = False
    submit_button = False
    cancel_button = False


    ## Form Inputs ##
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=100)
    phone = forms.CharField(required=True, max_length=11)
    address1 = forms.CharField(required=True, max_length=100)
    address2 = forms.CharField(required=False, max_length=100)
    city = forms.CharField(required=True, max_length=100)
    state = forms.ChoiceField(required=True, choices=STATE_CHOICES, widget=CustomSelect)
    ZIP = forms.CharField(required=True)