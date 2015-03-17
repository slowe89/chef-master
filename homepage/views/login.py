from django.conf import settings
from base_app.CustomForm import CustomForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django_mako_plus.controller import view_function
import base_app.models as hmod
from django_mako_plus.controller.router import get_renderer
from django.contrib.auth import authenticate, login, logout

templater = get_renderer('homepage')

##########################################################################################
################################### FORM CLASS ###########################################
##########################################################################################

class LoginForm(CustomForm):

	''' Class for the login form '''

	username = forms.CharField(required=True, max_length=100)
	password = forms.CharField(required=True, label="Password", widget=forms.PasswordInput)

	def clean(self):

		# Check to see if self is valid
		if self.is_valid():

			# See if username and password combo is correct
			user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])

			if user is None:
				raise forms.ValidationError("Incorrect Username and/or Password")

		return self.cleaned_data

##########################################################################################
################################## LOGIN USER ACTION #####################################
##########################################################################################

@view_function
def process_request(request):

	# Define the view bag
	params={}

	form = LoginForm(request)

	## IF POST METHOD OCCURRED ##
	if request.method == 'POST':

		form = LoginForm(request, request.POST)

		if form.is_valid():

			## Authenticate again
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

			login(request, user)

			return HttpResponse('<script>window.location.reload() = window.location.reload()</script>')

	params['form'] = form

	return templater.render_to_response(request, 'login.html', params)

##########################################################################################
################################## LOGOUT USER ACTION ####################################
##########################################################################################

@view_function
def logout_user(request):

	logout(request)

	return HttpResponseRedirect('/homepage/index/')

##########################################################################################
################################## LOGIN REQUIRED ####################################
##########################################################################################

@view_function
def required(request):


	return templater.render_to_response(request, 'loginRequired.html')

