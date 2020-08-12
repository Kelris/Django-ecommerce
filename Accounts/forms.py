from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "Email"}))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': "form-control", 'placeholder': "Username"})
        self.fields['password1'].widget.attrs.update({'class': "form-control", 'placeholder': "Password"})
        self.fields['password2'].widget.attrs.update({'class': "form-control", 'placeholder': "Password confirmation"})

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class AuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': "form-control", 'placeholder': "Username"})
        self.fields['password'].widget.attrs.update({'class': "form-control", 'placeholder': "Password"})
