from django.db.models.signals import post_save
from django.dispatch import receiver
from commandes.models import Order
from .models import Invoice

@receiver(post_save, sender=Order)
def create_invoice(sender, instance, created, **kwargs):

    """
    Crée automatiquement une facture quand la commande devient 'paid'
    """
    if instance.statuts=="paid":
        # Vérifie si la facture n'existe pas déjà
        if not hasattr(instance, 'invoice'):
            Invoice.objects.create(
                order=instance,
                total=instance.total
            )