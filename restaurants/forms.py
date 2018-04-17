from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'

        widgets = {
        	'opening_time': forms.TimeInput(attrs={'type':'time'}),
        	'closing_time': forms.TimeInput(attrs={'type':'time'}),
        }
