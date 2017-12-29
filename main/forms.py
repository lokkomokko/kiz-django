from django import forms
from django.forms import SelectDateWidget


class AuthorForm(forms.Form):

    field1 = forms.DateField(widget=SelectDateWidget(empty_label="Nothing", years=range(1970, 2020)))