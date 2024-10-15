from django import forms
from .models import Cash_box


class CashBoxForm(forms.ModelForm):
    class Meta:
        model = Cash_box
        fields = ['name', 'type', 'active_image', 'default_image', 'color']
