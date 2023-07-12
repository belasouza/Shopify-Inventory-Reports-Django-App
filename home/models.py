from django.db import models

# Create your models here.
class ItemManager(models.Manager):
    def create_item(self, s, inc, avlb):
        item = self.create(sku=s, incoming=inc, available=avlb)
        return item
    
class Item(models.Model):
    sku = models.CharField(max_length=10, unique=True)
    incoming = models.IntegerField()
    available = models.IntegerField() 

    objects = ItemManager()
    def __str__(self):
        return self.sku
    
