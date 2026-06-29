import asyncio
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import DemandeCompte, DemandeOperation, Compte
from .nats_admin import notifier_client, notifier_client_operation

def index(request):
    demandes = DemandeCompte.objects.filter(statut='EN_ATTENTE').order_by('-date_creation')
    demandes_op = DemandeOperation.objects.filter(statut='EN_ATTENTE').order_by('-operation__date_creation')
    return render(request, "app/index.html", {
        'demandes': demandes,
        'demandes_op': demandes_op
    })

def accepter_demande(request, demande_id):
    demande = get_object_or_404(DemandeCompte, id=demande_id)
    demande.statut = 'ACCEPTE'
    demande.save()
    notifier_client(demande.client_id, demande.action, 'ACCEPTE')
    return redirect('/app/')

def refuser_demande(request, demande_id):
    demande = get_object_or_404(DemandeCompte, id=demande_id)
    demande.statut = 'REFUSE'
    demande.save()
    notifier_client(demande.client_id, demande.action, 'REFUSE')
    return redirect('/app/')

@require_POST
def accepter_operation(request, demande_id):
    demande = get_object_or_404(DemandeOperation, id=demande_id)
    operation = demande.operation
    with transaction.atomic():
        if operation.type_op == 'DEPOT':
            operation.compte_source.solde += operation.montant
            operation.compte_source.save()
        elif operation.type_op == 'RETRAIT':
            operation.compte_source.solde -= operation.montant
            operation.compte_source.save()  
        elif operation.type_op == 'VIREMENT':
            operation.compte_source.solde -= operation.montant
            operation.compte_destination.solde += operation.montant
            operation.compte_source.save()
            operation.compte_destination.save()
        demande.statut = 'ACCEPTE'
        demande.save()
    notifier_client_operation(demande.client_id, operation.id, 'ACCEPTE')
    return redirect('/app/')

@require_POST
def refuser_operation(request, demande_id):
    demande = get_object_or_404(DemandeOperation, id=demande_id)
    demande.statut = 'REFUSE'
    demande.save()
    notifier_client_operation(demande.client_id, operation.id, 'REFUSE')
    return redirect('/app/')