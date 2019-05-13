from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm


class UserCustomAuthenticationForm(AuthenticationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        
    def __init__(self, *args, **kwargs):
        super(UserCustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            # 'id': 'user',
            'class': 'input',})
        self.fields['password'].widget = forms.TextInput(attrs={
            # 'id': 'pass',
            'class': 'input',
            'type' : "password",
        })

class UserCustomCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'email',)
    
    def __init__(self, *args, **kwargs):
        super(UserCustomCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'id': 'user',
            'class': 'input',})
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'id': 'pass',
            'class': 'input',
            'type' : "password",
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'id': 'pass',
            'class': 'input',
            'type' : "password",
        })
        self.fields['email'].widget = forms.TextInput(attrs={
            'id': 'pass',
            'class': 'input',
            # 'type' : "email",
        })
        
    
class UserCustomChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name',)
