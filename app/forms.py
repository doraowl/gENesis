from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Логин'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Пароль'}))


class TextInputForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'mynamefield'}))
    text = forms.CharField(widget=forms.Textarea(
        attrs={'id': 'mytextfield'}))


class TestGenForm(forms.Form):
    text = forms.ChoiceField()
    theme = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'number', 'style': '  min-width: 100%;max-width: 100% ;'}))
