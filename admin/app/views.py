import asyncio
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import DemandeCompte
from .nats_admin import notifier_client  # On utilise le helper synchrone créé précédemment

def index(request):
    # On ne récupère que les demandes encore en attente
    demandes = DemandeCompte.objects.filter(statut='EN_ATTENTE').order_by('-date_creation')
    return render(request, "app/index.html", {'demandes': demandes})

def accepter_demande(request, demande_id):
    demande = get_object_or_404(DemandeCompte, id=demande_id)
    
    # 1. Mise à jour de la BDD Admin (Remplacement de traite=True)
    demande.statut = 'ACCEPTE'
    demande.save()
    
    # 2. Notification du client via NATS (Sujet: client.updates)
    notifier_client(demande.client_id, demande.action, 'ACCEPTE')
    
    return redirect('/app/')

def refuser_demande(request, demande_id):
    demande = get_object_or_404(DemandeCompte, id=demande_id)
    
    # 1. Mise à jour de la BDD Admin (Remplacement de traite=True)
    demande.statut = 'REFUSE'
    demande.save()
    
    # 2. Notification du client via NATS (Sujet: client.updates)
    notifier_client(demande.client_id, demande.action, 'REFUSE')
    
    return redirect('/app/')