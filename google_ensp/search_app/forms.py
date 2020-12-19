from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(
        max_length=5000,
        widget=forms.TextInput(attrs={"placeholder":"Que désirez vous chercher?","autocomplete":"off"}),
        required=True
    )
