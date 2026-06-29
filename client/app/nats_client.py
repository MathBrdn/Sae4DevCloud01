import asyncio
import nats
import json

async def publier_evenement_nats(action_type, user_id, details_dict):
    """
    Envoie un message standardisé sur le sujet NATS 'admin.alerts'
    pour la gestion des comptes.
    """
    try:
        nc = await nats.connect("nats://nats:4222")
        payload = {
            'user_id': user_id,
            'action': action_type,
            'details': details_dict
        }
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

async def publier_operation_nats(action_type, donnees_operation):
    """
    Envoie une demande d'opération financière sur le sujet NATS 'admin.alerts'
    """
    try:
        nc = await nats.connect("nats://nats:4222")
        payload = {
            'user_id': donnees_operation.get('client_id'),
            'action': action_type,
            'details': donnees_operation
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