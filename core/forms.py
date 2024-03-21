from django import forms


class InputForm(forms.Form):
    gamename = forms.CharField(max_length=200, required=False,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Enter a Game from Steam"}))
    