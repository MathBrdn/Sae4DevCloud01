from django.forms import ModelForm
from .models import Compte

class CompteForm(ModelForm):
    class Meta:
        model = Compte
        # On demande uniquement le nom et le solde initial au client
        fields = ['nom', 'solde']