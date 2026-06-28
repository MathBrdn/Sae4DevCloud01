from django.db import models

class Compte(models.Model):
    numero_compte = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100, default="Compte sans nom")
    solde = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    statut = models.CharField(max_length=50, default="EN_ATTENTE")
    client = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )