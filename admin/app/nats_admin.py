import asyncio
import nats
import json

async def publier_decision_nats(user_id, action_type, statut_decision):
    """
    Envoie un message standardisé sur le sujet NATS 'client.updates'
    pour informer le client de la décision de l'administrateur.
    """
    try:
        # Connexion au conteneur NATS via le réseau Docker
        nc = await nats.connect("nats://nats:4222")
        
        # Structuration du message JSON attendu par le client-worker
        payload = {
            'user_id': user_id,
            'action': action_type, # 'CREATE', 'UPDATE', ou 'DELETE'
            'statut': statut_decision # 'ACCEPTE' ou 'REFUSE'
        }
        
        # Envoi des données encodées en bytes sur le bon canal
        await nc.publish("client.updates", json.dumps(payload).encode('utf-8'))
        await nc.flush()
        await nc.close()
    except Exception as e:
        print(f"Erreur d'envoi NATS Admin vers Client (User {user_id}) : {e}")

def notifier_client(user_id, action_type, statut_decision):
    """
    Helper synchrone appelé directement dans admin/app/views.py
    pour exécuter la publication sans casser le flux synchrone de Django.
    """
    asyncio.run(publier_decision_nats(user_id, action_type, statut_decision))