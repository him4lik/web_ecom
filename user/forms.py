from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date

class LoginForm(forms.Form):
    phone = forms.CharField(
        label="Phone Number",
        max_length=15,
        widget=forms.TextInput(attrs={"placeholder": "Enter phone number"})
    )
    otp = forms.CharField(
        label="OTP",
        max_length=6,
        required=False,  # Initially hidden, will be enabled via JavaScript
        widget=forms.TextInput(attrs={"placeholder": "Enter OTP", "style": "display:none;"})
    )

class ProfileForm(forms.Form):
    name = forms.CharField(
        label="Full Name",
        max_length=30,
        widget=forms.TextInput(attrs={ 'class': 'form-control', "placeholder": "Enter Full Name"})
    )
    email = forms.CharField(
        label="Email",
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={ 'class': 'form-control', "placeholder": "Enter Email"})
    )
    dob = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'Select your date of birth'
        }),
        validators=[
            MaxValueValidator(limit_value=date.today(), message="Date of birth cannot be in the future")        ]
    )

class AddressForm(forms.Form):
    type = forms.ChoiceField(
        label="Address Type",
        required = True,
        choices=[
            ('Home', 'Home'),
            ('Office', 'Office'), 
            ('Friend', 'Friend'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        label="Name",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={ 'class': 'form-control', "placeholder": "Enter Name"})
    )
    phone = forms.CharField(
        label="Full Name",
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={ 'class': 'form-control', "placeholder": "Enter Phone Number"})
    )
    line1 = forms.CharField(
        label="Line 1",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={ 'class': 'form-control', "placeholder": "Line 1"})
    )
    line2 = forms.CharField(
        label="Line 2",
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={ 'class': 'form-control', "placeholder": "Line 2"})
    )
    city = forms.CharField(
        label="City",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={ 'class': 'form-control', "placeholder": "Enter City"})
    )
    state = forms.CharField(
        label="State",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={ 'class': 'form-control', "placeholder": "Enter State"})
    )
    pin = forms.CharField(
        label="Pin Code",
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={ 'class': 'form-control', "placeholder": "Enter PinCode"})
    )
    landmark = forms.CharField(
        label="Landmark",
        max_length=30,
        widget=forms.TextInput(attrs={ 'class': 'form-control', "placeholder": "Enter Landmark"})
    )
    
    