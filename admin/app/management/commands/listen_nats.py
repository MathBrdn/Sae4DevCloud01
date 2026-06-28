import asyncio
import json
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async  # <-- Bien présent
from nats.aio.client import Client as NATS
from app.models import DemandeCompte 

# On crée la fonction de sauvegarde en dehors pour être 100% sûr que Django l'isole
@sync_to_async
def save_demande(data):
    return DemandeCompte.objects.create(
        action=data.get('action'),
        client_id=data.get('user_id'),
        data_payload=data.get('details')
    )

class Command(BaseCommand):
    help = "Écoute les messages NATS et les enregistre en BDD"

    def handle(self, *args, **options):
        self.stdout.write("Démarrage du listener NATS...")
        try:
            asyncio.run(self.main())
        except KeyboardInterrupt:
            self.stdout.write("\nListener arrêté.")

    async def main(self):
        nc = NATS()
        await nc.connect("nats://nats:4222")
        self.stdout.write(self.style.SUCCESS("Connecté à NATS. Écoute sur 'admin.alerts'..."))

        async def message_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                self.stdout.write(f"Message reçu de NATS : {data}")

                # Appel de la fonction décorée avec "await"
                await save_demande(data)
                
                self.stdout.write(self.style.SUCCESS(f"Demande [{data.get('action')}] enregistrée !"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erreur lors du traitement : {e}"))

        await nc.subscribe("admin.alerts", cb=message_handler)

        while True:
            await asyncio.sleep(1)