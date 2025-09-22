from api.models import Product

from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Product)
def cache_invalidation(sender, instance, **kwargs):
    """
    Signal handler to invalidate cached product list data.

    This function deletes all cache entries matching the pattern "*product_list*".
    It is intended to be connected to model signals (e.g., post_save, post_delete)
    to ensure that cached product lists are refreshed when relevant model instances
    are created, updated, or deleted.

    Args:
        sender: The model class that sent the signal.
        instance: The instance of the model that triggered the signal.
        **kwargs: Additional keyword arguments passed by the signal.
    """
    cache.delete_pattern("*product_list*")  # type: ignore

