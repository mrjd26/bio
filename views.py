from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from forms import login_form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from google.appengine.api import mail
from emailusernames.utils import create_user, get_user, user_exists
import uuid
from bio.models import Verify

def auth_login(request):
  """
  site email & password login handling

  Args: None
  Returns:
      my_account view on success or error messages
  """
  message=''

  if request.method == 'POST':
    form = login_form(request.POST)
	
    if form.is_valid():
      email = request.POST['email']
      password = request.POST['password']	    
      user = authenticate(
                             email = email,
                             password = password
                         )
	    
      if user is not None:
        if user.is_active:
          login(
                   request,
                   user
               )
          return redirect('/my_account/')
        else:
          message = ('disabled account or email confimation needed: '
                     '\n click the link sent to ' + email + ' to activate'
                     '\n your account.')	    
          #return a 'disabled account' error message
      else:
        message = 'Email or Password incorrect'
        #return an invalid login error message.
  else:
    form = login_form()

  return render(request,'login.html',{
                                         'form': form,
                                         'message': message,
                                         'registration': False
                                     })

def registration(request):
  """
  a view to handle user registration on site
  ** still needs double user registration error handling
  ** and forgot password ? functionality

  Args: None
  Returns: 
      on valid registration...HttpResponse
      notifiying user to check for confirmation email
  """

  if request.method == 'POST':
    form = login_form(request.POST)
    
    if form.is_valid():
      email = request.POST['email']
      password = request.POST['password']

      #email verification from google
      if not mail.is_email_valid(email):
        # handle a non valid email address here
        pass
      else:
        create_user(email, password)
        
        u = User.objects.get(email = email)
        u.is_active = False
        u.save()
     
        token = uuid.uuid4()
        token = str(token)
        v = Verify(email = email, token = token)
        v.save()

        sender_address = ('Friendly Media Support'
                          '<friendlymedia.incorporation@gmail.com>')
        subject = 'Confirm your registration'
        body = ('Thank you fo creating an account!\n'
                'Please confirm your email address'
                'by clicking on the link below:\n %s'
                %('https://group-captain.appspot.com/confirmed?'
                  'email=' + email + '&token=' + token)
               )
        mail.send_mail(sender_address, email, subject, body)

        return HttpResponse('Thanks! A confirmation email has been '
                            'sent to ' + email + '. \n Click the link '
                            'in the email to activate your account.') 

  else:
    form = login_form()
  return render(request, 'login.html', {
                                           'form': form,
                                           'registration': True
                                       })

def confirmed(request):
  """
  view to handle link in email confimation
  if token in email verification matches token in User db
  activate the account

  Args: None
  Returns: logs user into account or redirect to sign in
  """    
  email = request.GET['email']
  token = request.GET['token']

  v = Verify.objects.get(email = email)
  if str(v.token) == token:
    user = User.objects.get(email = email)
    user.is_active = True
    user.save()
    user.backend = 'emailusernames.backends.EmailAuthBackend'
    login(request, user)
    return redirect('/my_account/')
  else:
   return HttpResponseNotFound('<h1>Page not found</h1>') 

def logout_view(request):
  logout(request)
  return redirect('/')
