from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True) 
    
    class Role(models.TextChoices):
        ADMIN = "Admin", "Admin"
        CLIENT = "Client", "Client"
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    
    class Meta:
        db_table = 'user'
        managed = False 


class Compte(models.Model):
    id = models.AutoField(primary_key=True)
    numero_compte = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100, default="Compte sans nom")
    solde = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    statut = models.CharField(max_length=50, default="EN_ATTENTE")
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'compte'
        managed = True 


class Operation(models.Model):
    id = models.AutoField(primary_key=True)
    
    TYPE_CHOICES = [
        ('DEPOT', 'Dépôt'),
        ('RETRAIT', 'Retrait'),
        ('VIREMENT', 'Virement'),
    ]
    type_op = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)
    compte_source = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='operations_sortantes')
    compte_destination = models.ForeignKey(Compte, on_delete=models.CASCADE, null=True, blank=True, related_name='operations_entrantes')

    class Meta:
        db_table = 'operation' 
        managed = True 