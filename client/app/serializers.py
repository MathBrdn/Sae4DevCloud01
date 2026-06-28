from rest_framework import serializers
from .models import Compte

class CompteNatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        # On ne prend que les champs nécessaires pour les requêtes NATS
        fields = ['id', 'nom', 'solde']
    def validate_solde(self, value):
        if value < 0:
            raise serializers.ValidationError("Le solde initial ne peut pas être négatif.")
        return value