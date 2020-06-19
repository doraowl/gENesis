from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import app.models


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
    text = forms.ChoiceField(widget=forms.Select())
    # theme = forms.CharField(widget=forms.TextInput(
    #   attrs={'type': 'number', 'value': 0, 'style': '  min-width: 100%;max-width: 100% ;'}))
    prepositions = forms.CharField(label='prepositions', widget=forms.TextInput(
        attrs={'type': 'number', 'value': 0, 'style': '  min-width: 100%;max-width: 100% ;'}))
    tenses = forms.CharField(label='tenses', widget=forms.TextInput(attrs={
                             'type': 'number', 'value': 0, 'style': '  min-width: 100%;max-width: 100% ;'}))

  #  def __init__(self, user, *args, **kwargs):
   #     self.user = user
    #    super(TestGenForm, self).__init__(*args, **kwargs)
    #   self.fields['text'].choices = [
    #      (h.id, h.name) for h in app.models.Text.objects.filter(user=self.user)]
