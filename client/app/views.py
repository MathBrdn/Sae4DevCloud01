from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from . import models
import time
from .forms import CompteForm
from .serializers import CompteNatsSerializer, OperationNatsSerializer 
from .nats_client import notifier_admin, notifier_admin_operation

def index(request, user_id):
    comptes = models.Compte.objects.filter(client_id=user_id)
    operations = models.Operation.objects.filter(
        Q(compte_source__client_id=user_id) | Q(compte_destination__client_id=user_id)
    ).order_by('-date_creation')
    
    return render(request, 'app/index.html', {'client': {'id': user_id}, 'comptes': comptes, 'operations': operations})

def create_compte(request, user_id):
    if request.method == "POST":
        lform = CompteForm(request.POST)
        if lform.is_valid():
            compte_local = lform.save(commit=False)
            compte_local.client_id = user_id
            compte_local.statut = 'EN_ATTENTE'
            compte_local.numero_compte = f"TEMP-{int(time.time() * 1000)}"
            compte_local.save()
            compte_local.numero_compte = str(compte_local.id)
            compte_local.save(update_fields=['numero_compte'])
            serializer = CompteNatsSerializer(data=lform.cleaned_data)
            if serializer.is_valid():
                donnees_compte = serializer.data
                donnees_compte['id'] = compte_local.id
                donnees_compte['numero_compte'] = compte_local.numero_compte
                notifier_admin('CREATE', user_id, donnees_compte)
                return redirect(f'/app/{user_id}/')
    else:
        lform = CompteForm()
    return render(request, "app/create_compte.html", {"form": lform, "user_id": user_id})

def affiche_compte(request, user_id, id):
    compte = get_object_or_404(models.Compte, pk=id, client_id=user_id)
    return render(request, "app/traitement_compte.html", {"compte": compte})

def update_compte(request, user_id, compte_id):
    compte = get_object_or_404(models.Compte, pk=compte_id, client_id=user_id)
    if request.method == "POST":
        lform = CompteForm(request.POST, instance=compte)
        if lform.is_valid():
            compte_local = lform.save(commit=False)
            compte_local.statut = 'EN_ATTENTE'
            compte_local.save()
            serializer = CompteNatsSerializer(data=lform.cleaned_data)
            if serializer.is_valid():
                donnees_compte = serializer.data
                donnees_compte['id'] = compte_id
                notifier_admin('UPDATE', user_id, donnees_compte)
                return redirect(f'/app/{user_id}/')
    else:
        lform = CompteForm(instance=compte)
    return render(request, "app/update_compte.html", {"form": lform, "user_id": user_id, "compte_id": compte_id})

def delete_compte(request, user_id, compte_id):
    compte = get_object_or_404(models.Compte, pk=compte_id, client_id=user_id)
    if request.method == "POST":
        compte.statut = 'EN_ATTENTE'
        compte.save()
        donnees_payload = {
            'id': compte.id,
            'nom': compte.nom,
            'solde': str(compte.solde), 
            'motif': request.POST.get('motif', 'Clôture demandée par le client')
        }
        notifier_admin('DELETE', user_id, donnees_payload)
        return redirect(f'/app/{user_id}/') 
    return render(request, "app/delete_compte.html", {"user_id": user_id, "compte": compte})

def create_operation(request, user_id):
    if request.method == "POST":
        type_op = request.POST.get('type_op')
        montant = request.POST.get('montant')
        src_id = request.POST.get('compte_source')
        dest_id = request.POST.get('compte_destination') or None
        compte_src = get_object_or_404(models.Compte, id=src_id, client_id=user_id)
        compte_dest = get_object_or_404(models.Compte, id=dest_id) if dest_id else None
        operation = models.Operation.objects.create(type_op=type_op, montant=montant, compte_source=compte_src, compte_destination=compte_dest)
        models.DemandeOperation.objects.create(operation=operation, client_id=user_id, statut='EN_ATTENTE')
        payload = {
            'operation_id': operation.id, 
            'client_id': int(user_id), 
            'type_op': type_op, 
            'montant': float(montant), 
            'compte_source_id': compte_src.id, 
            'compte_destination_id': compte_dest.id if compte_dest else None
        }
        serializer = OperationNatsSerializer(data=payload)
        if serializer.is_valid():
            notifier_admin_operation('CREATE_OP', serializer.data)  
        return redirect(f'/app/{user_id}/')   
    comptes = models.Compte.objects.filter(client_id=user_id, statut='ACCEPTE')
    tous_les_comptes = models.Compte.objects.filter(statut='ACCEPTE')
    return render(request, "app/create_operation.html", {"comptes": comptes, "tous_les_comptes": tous_les_comptes, "user_id": user_id})