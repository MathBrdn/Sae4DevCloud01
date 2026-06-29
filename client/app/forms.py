from django.forms import ModelForm
from .models import Compte

class CompteForm(ModelForm):
    class Meta:
        model = Compte
        fields = ['nom', 'solde']