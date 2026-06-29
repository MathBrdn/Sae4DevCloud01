import asyncio
import nats
import json

# =====================================================================
# 1. GESTION DES COMPTES (Déjà existant)
# =====================================================================
async def publier_decision_nats(user_id, action_type, statut_decision):
    """
    Envoie un message standardisé sur le sujet NATS 'client.updates'
    pour informer le client de la décision de l'administrateur concernant un compte.
    """
    try:
        nc = await nats.connect("nats://nats:4222")
        
        payload = {
            'user_id': user_id,
            'action': action_type,       # 'CREATE', 'UPDATE', ou 'DELETE'
            'statut': statut_decision    # 'ACCEPTE' ou 'REFUSE'
        }
        
        await nc.publish("client.updates", json.dumps(payload).encode('utf-8'))
        await nc.flush()
        await nc.close()
    except Exception as e:
        print(f"Erreur d'envoi NATS Admin vers Client (User {user_id}) : {e}")

def notifier_client(user_id, action_type, statut_decision):
    """
    Helper synchrone appelé directement dans admin/app/views.py pour les comptes.
    """
    asyncio.run(publier_decision_nats(user_id, action_type, statut_decision))


# =====================================================================
# 2. 🚀 AJOUT : GESTION DES OPÉRATIONS BANCAIRES (Dépôts, Retraits, Virements)
# =====================================================================
async def publier_decision_operation_nats(client_id, operation_id, statut_decision):
    """
    Envoie un message sur le sujet NATS 'client.operations'
    pour informer le client-worker de la validation/refus d'une opération financière.
    """
    try:
        # Connexion à NATS
        nc = await nats.connect("nats://nats:4222")
        
        # Payload attendu pour mettre à jour le solde et la demande côté client
        payload = {
            'client_id': client_id,
            'operation_id': operation_id,
            'statut': statut_decision  # 'ACCEPTE' ou 'REFUSE'
        }
        
        # Envoi sur le canal dédié aux opérations
        await nc.publish("client.operations", json.dumps(payload).encode('utf-8'))
        await nc.flush()
        await nc.close()
    except Exception as e:
        print(f"Erreur d'envoi NATS Admin (Opération {operation_id}) : {e}")

def notifier_client_operation(client_id, operation_id, statut_decision):
    """
    Helper synchrone appelé dans views.py : accepter_operation et refuser_operation
    """
    asyncio.run(publier_decision_operation_nats(client_id, operation_id, statut_decision))