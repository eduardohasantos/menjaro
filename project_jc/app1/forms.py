from django import forms
from .models import NewsletterSubscription

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "id": "id_email",
                    "placeholder": "seuemail@exemplo.com",
                    "required": True,
                }
            )
        }
        labels = {"email": "E-mail"}
