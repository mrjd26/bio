from django import forms

class login_form(forms.Form):
  email = forms.CharField(
      max_length = 50,
      label = "",
      widget = forms.TextInput(attrs = {'placeholder' : 'Email'})
  )
  
  password = forms.CharField(
      max_length = 50,
      label = "",
      widget = forms.PasswordInput(attrs = {'placeholder' : 'Password'})
  )
