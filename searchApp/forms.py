from django import forms

class searchForms(forms.Form):
    current_search = forms.CharField(label='search', max_length=100)