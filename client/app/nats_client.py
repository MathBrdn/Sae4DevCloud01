import asyncio
import nats
import json

async def publier_evenement_nats(action_type, user_id, details_dict):
    """
    Envoie un message standardisé sur le sujet NATS 'demandes.comptes'
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
        await nc.publish("demandes.comptes", json.dumps(payload).encode('utf-8'))
        await nc.flush()
        await nc.close()
    except Exception as e:
        print(f"Erreur d'envoi NATS [{action_type}] : {e}")

def notifier_admin(action_type, user_id, details_dict):
    """
    Helper synchrone pour exécuter la fonction asynchrone sans bloquer les vues Django
    """
    asyncio.run(publier_evenement_nats(action_type, user_id, details_dict))