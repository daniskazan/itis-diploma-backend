from django import forms


class ActivateGrantForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
