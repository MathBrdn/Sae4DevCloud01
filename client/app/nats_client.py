import asyncio
import nats
import json

# =====================================================================
# 1. GESTION DES COMPTES (Déjà existant)
# =====================================================================
async def publier_evenement_nats(action_type, user_id, details_dict):
    """
    Envoie un message standardisé sur le sujet NATS 'admin.alerts'
    pour la gestion des comptes.
    """
    try:
        # Connexion au conteneur NATS via son nom de service docker-compose
        nc = await nats.connect("nats://nats:4222")
        
        # Structuration du message JSON
        payload = {
            'user_id': user_id,
            'action': action_type,
            'details': details_dict
        }
        
        # Envoi des données converties en octets (bytes)
        await nc.publish("admin.alerts", json.dumps(payload).encode('utf-8'))
        await nc.flush()
        await nc.close()
    except Exception as e:
        print(f"Erreur d'envoi NATS [{action_type}] : {e}")

def notifier_admin(action_type, user_id, details_dict):
    """
    Helper synchrone pour exécuter la fonction asynchrone sans bloquer les vues Django
    """
    asyncio.run(publier_evenement_nats(action_type, user_id, details_dict))


# =====================================================================
# 2. GESTION DES OPÉRATIONS BANCAIRES
# =====================================================================
async def publier_operation_nats(action_type, donnees_operation):
    """
    Envoie une demande d'opération financière sur le sujet NATS 'admin.alerts'
    """
    try:
        nc = await nats.connect("nats://nats:4222")
        
        # Structuration cohérente avec ce que l'admin reçoit pour les alertes
        payload = {
            'user_id': donnees_operation.get('client_id'),
            'action': action_type,  # 'CREATE_OP'
            'details': donnees_operation  # Contient l'ID de l'opération, le montant, etc.
        }
        
        await nc.publish("admin.alerts", json.dumps(payload).encode('utf-8'))
        await nc.flush()
        await nc.close()
    except Exception as e:
        print(f"Erreur d'envoi NATS Client (Opération) : {e}")

def notifier_admin_operation(action_type, donnees_operation):
    """
    Helper synchrone appelé directement dans client/app/views.py pour les opérations
    """
    asyncio.run(publier_operation_nats(action_type, donnees_operation))