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
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemManager()
    def __str__(self):
        return self.sku

class UpdateManager(models.Manager):
    def new_update(self):
        update = self.create()
        return update
    
class Update(models.Model):
    updated_at = models.DateField(auto_now=True)
    objects = UpdateManager()
    def __str__(self):
        return str(self.updated_at)
    def set_date_now(self):
       self.updated_at = models.DateField(auto_now=True) 