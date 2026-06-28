from django.db import models

class Compte(models.Model):
    numero_compte = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100, default="Compte sans nom")
    solde = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    statut = models.CharField(max_length=50, default="EN_ATTENTE")
    client = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    class Meta:
        db_table = 'compte'
        managed = False

class DemandeCompte(models.Model):
    TYPE_ACTION = [
        ('CREATE', 'Création'),
        ('UPDATE', 'Modification'),
        ('DELETE', 'Suppression'),
    ]
    
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('ACCEPTE', 'Accepté'),
        ('REFUSE', 'Refusé'),
    ]

    action = models.CharField(max_length=10, choices=TYPE_ACTION)
    client_id = models.IntegerField()
    data_payload = models.JSONField() 
    # Remplacement de traite par statut
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demande_compte'  # <-- On force le nom de la table ici

    def __str__(self):
        return f"{self.action} - Client {self.client_id} [{self.statut}]"