from django import forms
from .models import NewsletterSubscription,Comentario
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 

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

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Escreva seu comentário aqui...'
            }),
        }
        labels = {'texto': 'Comentário'}

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
