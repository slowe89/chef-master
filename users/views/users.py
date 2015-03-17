'''

    Author: John Turner
    Version: 2.0
    Last Updated: 2/28/2015

    View for all CRUD functions for the Users.

'''

from django.conf import settings
from base_app.CustomForm import CustomForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django_mako_plus.controller import view_function
from django.contrib.auth.decorators import permission_required
import base_app.models as hmod
from django_mako_plus.controller.router import get_renderer
from django.utils.translation import ugettext as _
from base_app.CustomWidgets import CustomSelect, CustomRadioRenderer
from django.contrib.auth import authenticate, login, logout

templater = get_renderer('users')

##########################################################################################
################################### FORM CLASS ###########################################
##########################################################################################


class UserEditForm(CustomForm):

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
    title = "User Information"
    link = "users/users"

    ## Form Inputs ##
    username = forms.CharField(required=True, max_length=100)
    password = forms.CharField(required=False, max_length=100, widget=forms.PasswordInput)
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=100)
    phone = forms.CharField(required=True, max_length=11)
    address1 = forms.CharField(required=True, max_length=100)
    address2 = forms.CharField(required=False, max_length=100)
    city = forms.CharField(required=True, max_length=100)
    state = forms.ChoiceField(required=True, choices=STATE_CHOICES, widget=CustomSelect)
    ZIP = forms.CharField(required=True)
    security_question = forms.CharField(required=True, max_length=100)
    security_answer = forms.CharField(required=True, max_length=100)
    group = forms.ModelChoiceField(required=False, queryset=hmod.Group.objects.all().order_by('name'), widget=forms.RadioSelect(renderer=CustomRadioRenderer), empty_label=None)
    group_hidden = forms.CharField(required=True, widget=forms.HiddenInput(attrs={'id':'group_name'}))

    # Validation for the User name field
    def clean_username(self):

        # Test for short usernames
        if len(self.cleaned_data['username']) < 5:
            raise forms.ValidationError(_("Please enter a username greater than 5 characters."))

        # Test for duplicate usernames
        user = hmod.User.objects.filter(username = self.cleaned_data['username']).exclude(id=self.request.urlparams[0])

        if user.count() > 0:
            raise forms.ValidationError(_("This username already exists."))

        return self.cleaned_data['username']

    # Validation for the password field if user is being created for the first time
    def clean_password(self):

        # if the password field is blank, and the password stored in the database is blank
        # then require a new password to be set
        db_user = hmod.User.objects.filter(id=self.request.urlparams[0])

        if db_user[0].check_password('') and self.cleaned_data['password'] == '':
            raise forms.ValidationError("Please enter a password for this new user.")

        return self.cleaned_data['password']

##########################################################################################
################################# DEFAULT ACTION #########################################
##########################################################################################

@view_function
@permission_required('base_app.change_user', login_url='/homepage/login/')
def process_request(request):

    # Define the view bag
    params = {}

    # Delete all users that exist in the database with usernames = ''
    # (when someone starts a user and abandons it)
    users = hmod.User.objects.filter(username='').delete()

    # Delete all groups that might exist that are blank with no names:
    groups = hmod.Group.objects.filter(name='').delete()

    # Grab all the users from the database
    users = hmod.User.objects.all().order_by('last_name')

    # Add users to the view bag
    params['users'] = users

    return templater.render_to_response(request, 'users.html', params)

##########################################################################################
################################## EDIT USER ACTION ######################################
##########################################################################################

@view_function
@permission_required('base_app.change_user', login_url='/homepage/login/')
def edit(request):

    # Define the view bag
    params={}

    # Layout of the urls:
    #
    # /homepage/user.edit/a/b/c/d/e...
    #
    # request.urlparams[n] = everything after the <appname>/<filename>/
    #
    # For example [0] = a, [1] = b...

    # Delete any new groups that might have been added that need to be deleted:
    group = hmod.Group.objects.filter(name='').delete()

    try:
        user = hmod.User.objects.get(id=request.urlparams[0])
    except hmod.User.DoesNotExist:
        return HttpResponseRedirect('/users/users/')

    # Pass in user data to the form
    form = UserEditForm(request, initial={
        'username': user.username,
        'password': '',
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'address1': user.address1,
        'address2': user.address2,
        'city': user.city,
        'state': user.state,
        'ZIP': user.ZIP,
        'security_question': user.security_question,
        'security_answer': user.security_answer,
        'group': user.groups.all()[0],
        'group_name': user.groups.all()[0].name
        })

    if request.method == 'POST':

        # Validate the form
        form = UserEditForm(request, request.POST)

        if form.is_valid():

            # Update the object
            user.username = form.cleaned_data['username']

            if form.cleaned_data['password'] != '':
                user.set_password(form.cleaned_data['password'])

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.address1 = form.cleaned_data['address1']
            user.address2 = form.cleaned_data['address2']
            user.city = form.cleaned_data['city']
            user.state = form.cleaned_data['state']
            user.ZIP = form.cleaned_data['ZIP']
            user.security_question = form.cleaned_data['security_question']
            user.security_answer = form.cleaned_data['security_answer']

            # Delete the group that the user was a member of previously, then
            # add them to the new group
            user.groups.clear()

            try:
                group = hmod.Group.objects.get(name=form.cleaned_data['group_hidden'])
            except hmod.Group.DoesNotExist:
                raise forms.ValidationError("Please select a group!")
            group.user_set.add(user)

            # Save it to the database
            user.save()

            # Return user to list
            return HttpResponseRedirect('/users/users/')

    params['form'] = form

    return templater.render_to_response(request, 'EditUser.html', params)

##########################################################################################
################################ CREATE USER ACTION ######################################
##########################################################################################

@view_function
@permission_required('base_app.add_user', login_url='/homepage/login/')
def create(request):
    '''

        Creates a new user. First you have to create an address object and tie the user to the
        address.

    '''

    # Delete all users that exist in the database with usernames = ''
    # (when someone starts a user and abandons it)
    users = hmod.User.objects.filter(username='').delete()

    # Delete any new groups that might have been added that need to be deleted:
    group = hmod.Group.objects.filter(name='').delete()

    # Get Guest group for the new people
    try:
        group = hmod.Group.objects.get(name='Guest')
    except hmod.Group.DoesNotExist:
        HttpResponseRedirect('/users/users/')

    user = hmod.User()
    user.username = ''
    user.set_password('')
    user.first_name = ''
    user.last_name = ''
    user.email = ''
    user.phone = ''
    user.security_question = ''
    user.security_answer = ''
    user.address1 = ''
    user.address2 = ''
    user.city = ''
    user.state = ''
    user.ZIP = 0

    # Save to the db
    user.save()

    # Add to group
    group.user_set.add(user)

    # Redirect to the Edit page, with blank info
    return HttpResponseRedirect('/users/users.edit/{}/'.format(user.id))

##########################################################################################
################################ DELETE USER ACTION ######################################
##########################################################################################

@view_function
@permission_required('base_app.delete_user', login_url='/homepage/login/')
def delete(request):
    ''' Deletes a specific user '''

    # Try catch to see if the user exists
    try:
        user = hmod.User.objects.get(id=request.urlparams[0])
    except hmod.User.DoesNotExist:
        pass # User exists

    user.delete()

    return HttpResponseRedirect('/users/users/')

##########################################################################################
################################    SIGN UP FORM    ######################################
##########################################################################################
class NewUserEditForm(CustomForm):

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
    title = "User Information"
    link = "homepage/index"
    delete_button = False

    ## Form Inputs ##
    username = forms.CharField(required=True, max_length=100)
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=100)
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    phone = forms.CharField(required=True, max_length=11)
    address1 = forms.CharField(required=True, max_length=100)
    address2 = forms.CharField(required=False, max_length=100)
    city = forms.CharField(required=True, max_length=100)
    state = forms.ChoiceField(required=True, choices=STATE_CHOICES, widget=CustomSelect)
    ZIP = forms.CharField(required=True)
    security_question = forms.CharField(required=True, max_length=100)
    security_answer = forms.CharField(required=True, max_length=100)

    # Validation for the User name field
    def clean_username(self):

        # Test for short usernames
        if len(self.cleaned_data['username']) < 5:
            raise forms.ValidationError(_("Please enter a username greater than 5 characters."))

        # Test for duplicate usernames
        user = hmod.User.objects.filter(username = self.cleaned_data['username']).exclude(id=self.request.urlparams[0])

        if user.count() > 0:
            raise forms.ValidationError(_("This username already exists."))

        return self.cleaned_data['username']

    # Validation for the password field if user is being created for the first time
    def clean_password(self):

        # if the password field is blank, and the password stored in the database is blank
        # then require a new password to be set
        db_user = hmod.User.objects.filter(id=self.request.urlparams[0])

        if db_user[0].check_password('') and self.cleaned_data['password'] == '':
            raise forms.ValidationError("Please enter a password for this new user.")

        return self.cleaned_data['password']

##########################################################################################
################################ GUEST CREATES USER ######################################
##########################################################################################
@view_function
def create_new_user(request):
    '''

        Creates a new user. First you have to create an address object and tie the user to the
        address.

    '''

    # Delete all users that exist in the database with usernames = ''
    # (when someone starts a user and abandons it)
    users = hmod.User.objects.filter(username='').delete()

    # Delete any new groups that might have been added that need to be deleted:
    group = hmod.Group.objects.filter(name='').delete()

    # Get Guest group for the new people
    try:
        group = hmod.Group.objects.get(name='Guest')
    except hmod.Group.DoesNotExist:
        HttpResponseRedirect('/homepage/index/')

    user = hmod.User()
    user.username = ''
    user.set_password('')
    user.first_name = ''
    user.last_name = ''
    user.email = ''
    user.phone = ''
    user.security_question = ''
    user.security_answer = ''

    # Save to the db
    user.save()

    # Add to group
    group.user_set.add(user)

    # Redirect to the Edit page, with blank info
    return HttpResponseRedirect('/users/users.edit_new_user/{}/'.format(user.id))

##########################################################################################
################################## EDIT USER ACTION ######################################
##########################################################################################

@view_function
def edit_new_user(request):

    # Define the view bag
    params={}

    # Layout of the urls:
    #
    # /homepage/user.edit/a/b/c/d/e...
    #
    # request.urlparams[n] = everything after the <appname>/<filename>/
    #
    # For example [0] = a, [1] = b...

    # Delete any new groups that might have been added that need to be deleted:
    group = hmod.Group.objects.filter(name='').delete()

    try:
        user = hmod.User.objects.get(id=request.urlparams[0])
    except hmod.User.DoesNotExist:
        return HttpResponseRedirect('/users/users/')

    # Pass in user data to the form
    form = NewUserEditForm(request, initial={
        'username': user.username,
        'password': '',
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'address1': user.address1,
        'address2': user.address2,
        'city': user.city,
        'state': user.state,
        'ZIP': user.ZIP,
        'security_question': user.security_question,
        'security_answer': user.security_answer,
        'group': user.groups.all()[0],
        'group_name': user.groups.all()[0].name
        })

    if request.method == 'POST':

        # Validate the form
        form = NewUserEditForm(request, request.POST)

        if form.is_valid():

            # Update the object
            user.username = form.cleaned_data['username']

            if form.cleaned_data['password'] != '':
                user.set_password(form.cleaned_data['password'])

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.address1 = form.cleaned_data['address1']
            user.address2 = form.cleaned_data['address2']
            user.city = form.cleaned_data['city']
            user.state = form.cleaned_data['state']
            user.ZIP = form.cleaned_data['ZIP']
            user.security_question = form.cleaned_data['security_question']
            user.security_answer = form.cleaned_data['security_answer']

            # Save it to the database
            user.save()

            # Return user to list
            return HttpResponseRedirect('/users/newUserSuccess/')

    params['form'] = form

    return templater.render_to_response(request, 'newUser.html', params)

##########################################################################################
##################################  CHECK USERNAME  ######################################
##########################################################################################
@view_function
def check_username(request):

    username = request.REQUEST.get('username')

    check_name = hmod.User.objects.filter(username=username)

    if check_name.count() > 0:
        return HttpResponse('taken')
    else:
        return HttpResponse('available')

##########################################################################################
################################## EDIT MY ACCOUNT  ######################################
##########################################################################################
@view_function
def edit_my_account(request):

    # Define the view bag
    params={}

    # Layout of the urls:
    #
    # /homepage/user.edit/a/b/c/d/e...
    #
    # request.urlparams[n] = everything after the <appname>/<filename>/
    #
    # For example [0] = a, [1] = b...

    # Delete any new groups that might have been added that need to be deleted:
    group = hmod.Group.objects.filter(name='').delete()

    try:
        user = hmod.User.objects.get(id=request.user.id)
    except hmod.User.DoesNotExist:
        return HttpResponseRedirect('/homepage/index/')

    # Pass in user data to the form
    form = MyAccountEditForm(request, initial={
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'address1': user.address1,
        'address2': user.address2,
        'city': user.city,
        'state': user.state,
        'ZIP': user.ZIP,
        'security_question': user.security_question,
        'security_answer': user.security_answer,
        'group': user.groups.all()[0],
        'group_name': user.groups.all()[0].name
        })

    if request.method == 'POST':

        # Validate the form
        form = MyAccountEditForm(request, request.POST)

        if form.is_valid():

            # Update the object
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.address1 = form.cleaned_data['address1']
            user.address2 = form.cleaned_data['address2']
            user.city = form.cleaned_data['city']
            user.state = form.cleaned_data['state']
            user.ZIP = form.cleaned_data['ZIP']
            user.security_question = form.cleaned_data['security_question']
            user.security_answer = form.cleaned_data['security_answer']

            print('breaks here')
            # Save it to the database
            user.save()

            # Return user to list
            return HttpResponseRedirect('/homepage/index')

    params['form'] = form

    return templater.render_to_response(request, 'myAccount.html', params)

##########################################################################################
################################## NEW PASSWORD FORM #####################################
##########################################################################################
class NewPasswordForm(CustomForm):

    ''' Class for the form to be used in editing the password. '''

    ## Class title ##
    link = "users/users.edit_my_account/"
    delete_button = False

    ## Form Inputs ##
    curPassword = forms.CharField(required=False, max_length=100, widget=forms.PasswordInput)
    newPassword = forms.CharField(required=False, max_length=100, widget=forms.PasswordInput)
    newPassword2 = forms.CharField(required=False, max_length=100, widget=forms.PasswordInput)

    # Validation for the password field if user is being created for the first time
    def clean(self):

        # if the password field is blank, and the password stored in the database is blank
        # then require a new password to be set
        db_user = hmod.User.objects.filter(id=self.request.user.id)

        if db_user[0].check_password(self.cleaned_data['curPassword']):
            raise forms.ValidationError("Incorrect current password.")

        if self.cleaned_data['newPassword'] != self.cleaned_data['newPassword2']:
            raise forms.ValidationError("The new passwords doe not match.")

        return self.cleaned_data

##########################################################################################
##################################   EDIT PASSWORD  ######################################
##########################################################################################
@view_function
def edit_my_password(request):

    # Define the view bag
    params={}

    # Pass in user data to the form
    form = NewPasswordForm(request)

    if request.method == 'POST':

        # Validate the form
        form = NewPasswordForm(request, request.POST)

        try:
            user = hmod.User.objects.get(id=request.user.id)
        except hmod.User.DoesNotExist:
            return HttpResponse('Does not exist')

        if form.is_valid():

            user.set_password(form.cleaned_data['newPassword2'])
            user.save()
            login_user = authenticate(username=user.username, password=form.cleaned_data['newPassword2'])
            login(request, login_user)

            # Return user to list
            return HttpResponse('<script>$("#password_modal").modal("hide")</script>')

    params['form'] = form

    return templater.render_to_response(request, 'changePassword.html', params)

##########################################################################################
################################    My Account Form    ###################################
##########################################################################################
class MyAccountEditForm(CustomForm):

    ''' Class for the form to be used in editing the users. '''

    # List of constants for the states:
    ALASKA = 'AK'
    ALABAMA = 'AL'
    ARKANSAS = 'AR'
    ARIZONA = 'AZ'
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
        (ARIZONA, 'Arizona'),
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
    title = "User Information"
    link = "homepage/index"
    delete_button = False

    ## Form Inputs ##
    username = forms.CharField(required=True, max_length=100)
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=100)
    phone = forms.CharField(required=True, max_length=11)
    address1 = forms.CharField(required=True, max_length=100)
    address2 = forms.CharField(required=False, max_length=100)
    city = forms.CharField(required=True, max_length=100)
    state = forms.ChoiceField(required=True, choices=STATE_CHOICES, widget=CustomSelect)
    ZIP = forms.CharField(required=True)
    security_question = forms.CharField(required=True, max_length=100)
    security_answer = forms.CharField(required=True, max_length=100)

    # Validation for the User name field
    def clean_username(self):

        # Test for short usernames
        if len(self.cleaned_data['username']) < 5:
            raise forms.ValidationError(_("Please enter a username greater than 5 characters."))

        # Test for duplicate usernames
        user = hmod.User.objects.filter(username = self.cleaned_data['username']).exclude(id=self.request.user.id)

        if user.count() > 0:
            raise forms.ValidationError(_("This username already exists."))

        return self.cleaned_data['username']

    # Validation for the password field if user is being created for the first time
    def clean_password(self):

        # if the password field is blank, and the password stored in the database is blank
        # then require a new password to be set
        db_user = hmod.User.objects.filter(id=self.request.urlparams[0])

        if db_user[0].check_password('') and self.cleaned_data['password'] == '':
            raise forms.ValidationError("Please enter a password for this new user.")

        return self.cleaned_data['password']
