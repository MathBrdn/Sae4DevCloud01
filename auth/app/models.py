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
        managed = True 