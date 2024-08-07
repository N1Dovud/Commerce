from .models import Listing
from django import forms

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["category"]