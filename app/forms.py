from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from app.models import Sale, Product, AdditionalField


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('client_name', 'client_address', 'stage', 'manager')

    def clean_client_name(self):
        data = self.cleaned_data["client_name"]
        if "alex" in data:
            self.add_error("client_name", ValidationError("Name 'alex' are forbitten"))
        return data
    
    def clean_stage(self):
        data = self.cleaned_data["stage"]
        if data:
            return data
        else:
            return 'r'