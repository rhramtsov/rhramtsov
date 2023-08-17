from django import forms
from .models import ArtPiece
from auction.models import MyUser
from django.contrib.auth.forms import UserCreationForm


class ArtPieceForm(forms.ModelForm):
    class Meta:
        model = ArtPiece
        fields = ['name', 'collector', 'is_sold', 'price', 'minimum_price']



class MyUserRegistrationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'address', 'email', 'password1', 'password2']


