from django.shortcuts import render, get_object_or_404, redirect
from . import models
from .forms import CompteForm
from .serializers import CompteNatsSerializer 
from .nats_client import notifier_admin       

def index(request, user_id):
    comptes = models.Compte.objects.filter(client_id=user_id, statut="VALIDE")
    return render(request, 'app/index.html', {'client': {'id': user_id}, 'comptes': comptes})

# ==========================================
# 1. CRÉATION (POST)
# ==========================================
def create_compte(request, user_id):
    if request.method == "POST":
        lform = CompteForm(request.POST)
        if lform.is_valid():
            serializer = CompteNatsSerializer(data=lform.cleaned_data)
            if serializer.is_valid():
                donnees_compte = serializer.data
                notifier_admin('CREATE', user_id, donnees_compte)
                return redirect(f'/app/{user_id}/')
    else:
        lform = CompteForm()
        
    return render(request, "app/create_compte.html", {"form": lform, "user_id": user_id})

# ==========================================
# 2. AFFICHAGE (GET)
# ==========================================
def affiche_compte(request, user_id, id):
    compte = get_object_or_404(models.Compte, pk=id, client_id=user_id)
    return render(request, "app/traitement_compte.html", {"compte": compte})

# ==========================================
# 3. MODIFICATION (PUT)
# ==========================================
def update_compte(request, user_id, compte_id):
    compte = get_object_or_404(models.Compte, pk=compte_id, client_id=user_id)
    
    if request.method == "POST":
        lform = CompteForm(request.POST, instance=compte)
        if lform.is_valid():
            serializer = CompteNatsSerializer(data=lform.cleaned_data)
            if serializer.is_valid():
                donnees_compte = serializer.data
                donnees_compte['id'] = compte_id
                
                notifier_admin('UPDATE', user_id, donnees_compte)
                return redirect(f'/app/{user_id}/')
    else:
        lform = CompteForm(instance=compte)
        
    return render(request, "app/update_compte.html", {"form": lform, "user_id": user_id, "compte_id": compte_id})

# ==========================================
# 4. SUPPRESSION (DELETE)
# ==========================================
def delete_compte(request, user_id, compte_id):
    compte = get_object_or_404(models.Compte, pk=compte_id, client_id=user_id)
    
    if request.method == "POST":
        # Indentation corrigée ici 🚀
        donnees_payload = {
            'id': compte.id,
            'nom': compte.nom,
            'solde': str(compte.solde), 
            'motif': request.POST.get('motif', 'Clôture demandée par le client')
        }
        notifier_admin('DELETE', user_id, donnees_payload)
        return redirect(f'/app/{user_id}/')
        
    return render(request, "app/delete_compte.html", {"user_id": user_id, "compte": compte})