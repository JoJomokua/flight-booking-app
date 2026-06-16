import re
from django import forms
from django.core.exceptions import ValidationError

class BookingForm(forms.Form):
    name = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Joy Kanzi',
             'required': 'required',
             'pattern': r'^[a-zA-Z\s]+$',
            'title': 'Names can only contain letters and spaces.'
            })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'joy@example.com',
             'required': 'required',
            
            })
    )
    phone_number = forms.CharField(
        max_length=15, 
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. 0745678901',
            'pattern': r'^\+?[0-9]{7,14}$',
            'title': 'Please enter a valid phone number (7 to 14 digits, optional + prefix).'
            })
    )

    #  Validate Name Field
    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Check if name contains only letters and spaces
        if not re.match(r"^[a-zA-Z\s]+$", name):
            raise ValidationError("Names can only contain letters and spaces.")
        return name

    #  Validate Phone Number Field
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Strip out common formatting characters if users type them
        clean_phone = re.sub(r'[\s\-_\(\)]', '', phone_number)
        
        # Regex checks for an optional '+' followed by 7 to 14 digits
        if not re.match(r"^\+?[0-9]{7,14}$", clean_phone):
            raise ValidationError("Please enter a valid phone number (e.g., +1234567890).")
            
        return clean_phone