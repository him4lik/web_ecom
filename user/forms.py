from django import forms

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