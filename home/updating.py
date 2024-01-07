from home.models import Item, Update
from django.conf import settings
fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.INFO)


def get_item(s):
    try:
        found = Item.objects.get(sku=s)
        return found
    except Item.DoesNotExist:
        return False

def create_update():
    u = Update.objects.new_update()
    u.save()

def save_update(): # update number of items
    u = Update.objects.first()
    if u is None:
        create_update()
    else:
        u.set_date_now()

def update_database(data):
    new_items = []
    cur_items_lst = []
    for i,row in data.iterrows():
        item = get_item(row['SKU'])
        cur_items_lst.append(row['SKU'])
        if item:
            item.incoming = int(row['Incoming'])
            item.available = int(row['Available'])
            item.save()
        elif row['SKU'] != '': # need to add it to database
            # add to tmp list
            new_items.append(row)

    if len(new_items) != 0: # if there are items to add
        for item in new_items:
            new = Item.objects.create_item(item['SKU'],item['Incoming'], item['Available']) 
            new.save()
    
    total_items = len(new_items) + len(cur_items_lst)
    save_update()

    #return cur_items_lst