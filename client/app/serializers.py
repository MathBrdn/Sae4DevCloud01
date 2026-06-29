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

class OperationNatsSerializer(serializers.Serializer):
    operation_id = serializers.IntegerField()
    client_id = serializers.IntegerField()
    type_op = serializers.CharField(max_length=20)
    montant = serializers.FloatField()
    compte_source_id = serializers.IntegerField()
    compte_destination_id = serializers.IntegerField(required=False, allow_null=True)