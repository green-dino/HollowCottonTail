# playbook/forms.py
from django import forms

class PlaybookForm(forms.Form):
    play_name = forms.CharField(label='Play Name', max_length=100)
    roles = forms.CharField(label='Roles', widget=forms.Textarea)
    blocks = forms.CharField(label='Blocks', widget=forms.Textarea)
    tasks = forms.CharField(label='Tasks', widget=forms.Textarea)
    version = forms.CharField(label='Version', max_length=20)
    author = forms.CharField(label='Author', max_length=100)
