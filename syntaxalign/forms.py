from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Lead

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name','email','message']
from django import forms
from .models import DesignInquiry

class DesignInquiryForm(forms.ModelForm):
    class Meta:
        model = DesignInquiry
        fields = '__all__'

    def clean_proposed_offer(self):
        value = self.cleaned_data['proposed_offer']
        if not value.replace('$','').replace('.','').isdigit():
            raise forms.ValidationError("Proposed offer must be a number")
        return value
from django import forms
from .models import PurchaseRequest, Product

class PurchaseRequestForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        fields = ['product', 'email', 'whatsapp']

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data['whatsapp']
        if not whatsapp.isdigit() or len(whatsapp) < 8:
            raise forms.ValidationError("Enter a valid WhatsApp number.")
        return whatsapp
