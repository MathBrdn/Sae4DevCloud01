import asyncio
import json
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
from nats.aio.client import Client as NATS
from app.models import Compte

@sync_to_async
def mettre_a_jour_statut_compte(data):
    user_id = data.get('user_id')
    nouveau_statut = data.get('statut')
    compte = Compte.objects.filter(client_id=user_id, statut='EN_ATTENTE').first()
    
    if compte:
        compte.statut = nouveau_statut
        compte.save()
        return compte
    return None

class Command(BaseCommand):
    help = "Écoute les retours de l'admin via NATS pour mettre à jour le statut des comptes client"

    def handle(self, *args, **options):
        self.stdout.write("Démarrage du listener NATS Client...")
        try:
            asyncio.run(self.main())
        except KeyboardInterrupt:
            self.stdout.write("\nListener arrêté.")

    async def main(self):
        nc = NATS()
        await nc.connect("nats://nats:4222")
        self.stdout.write(self.style.SUCCESS("Connecté à NATS. Écoute sur 'client.updates'..."))

        async def message_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                self.stdout.write(f"Message de mise à jour reçu de l'admin : {data}")
                compte_modifie = await mettre_a_jour_statut_compte(data)
                if compte_modifie:
                    self.stdout.write(self.style.SUCCESS(
                        f"Le compte de l'utilisateur {data.get('user_id')} est maintenant : {data.get('statut')}"
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Aucun compte en attente trouvé pour l'utilisateur {data.get('user_id')}"
                    ))        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erreur lors du traitement du message client : {e}"))
        await nc.subscribe("client.updates", cb=message_handler)
        while True:
            await asyncio.sleep(1)

@sync_to_async
def traiter_retour_operation(data):
    op_id = data.get('operation_id')
    statut_admin = data.get('statut')
    demande = DemandeOperation.objects.filter(operation_id=op_id, statut='EN_ATTENTE').first()
    if demande:
        demande.statut = statut_admin
        demande.save()
        if statut_admin == 'ACCEPTE':
            op = demande.operation
            if op.type_op == 'DEPOT':
                op.compte_source.solde += op.montant
            elif op.type_op == 'RETRAIT':
                op.compte_source.solde -= op.montant
            elif op.type_op == 'VIREMENT':
                op.compte_source.solde -= op.montant
                op.compte_destination.solde += op.montant
            op.compte_source.save()
            if op.compte_destination:
                op.compte_destination.save()