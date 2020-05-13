from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):

    firstname = forms.CharField(max_length=100,required=True)
    lastname  = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(max_length=250,help_text='examples@putlook.com')

    class Meta:
        #ผูกค่ากับ Model
        model = User
        #ระบุ Column
        fields={'first_name','last_name','username','password','password2'}
