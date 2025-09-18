from api.models import Product

from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Product)
def cache_invalidation(sender, instance, **kwargs):
    """
    Signal receiver that invalidates cache when a Product instance is saved or deleted.

    This function listens to both the post_save and post_delete signals for the Product model.
    When triggered, it prints a message indicating that the cache is being cleared.

    Args:
        sender (Model): The model class that sent the signal (Product).
        instance (Product): The instance of Product that was saved or deleted.
        **kwargs: Additional keyword arguments passed by the signal.
    """

    #! Clear Product List Cache
    cache.delete_pattern("*product_list*")  # type: ignore

    print("CLEARING CACHE...")
