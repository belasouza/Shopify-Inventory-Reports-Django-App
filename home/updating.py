from home.models import Item, NumUpdated
import logging
from django.conf import settings
fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.INFO)

logging.basicConfig(format=fmt, level=lvl)

def get_item(s):
    try:
        found = Item.objects.get(sku=s)
        return found
    except Item.DoesNotExist:
        return False

def create_update(n):
    u = NumUpdated.objects.new_update(n)
    u.save()
    logging.info("saved new NumUpdated object")

def update_noi(n): # update number of items
    u = NumUpdated.objects.first()
    if u is None:
        logging.info("creating new NumUpdated object")
        create_update(n)
    else:
        u.items_updated = n
        u.save()
        logging.info("updated NumUpdated object")

def update_database(data):
    new_items = []
    cur_items_lst = []
    for i,row in data.iterrows():
        item = get_item(row['SKU'])
        cur_items_lst.append(row['SKU'])
        if item:
            logging.info("Updating...")
            item.incoming = int(row['Incoming'])
            item.available = int(row['Available'])
            item.save()
        else: # need to add it to database
            # add to tmp list
            logging.info("Item needs to be added")
            new_items.append(row)

    if len(new_items) != 0: # if there are items to add
        for item in new_items:
            logging.info("Adding...")
            new = Item.objects.create_item(item['SKU'],item['Incoming'], item['Available']) 
            new.save()
            logging.info("Added" + new.sku)
    
    total_items = len(new_items) + len(cur_items_lst)
    update_noi(total_items)

    #return cur_items_lst