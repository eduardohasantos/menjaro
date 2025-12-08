from .forms import SubscriptionForm

def subscription_form(request):
    return {"form_subscription": SubscriptionForm()}

