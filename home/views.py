from time import sleep
from django.http import StreamingHttpResponse
from django.shortcuts import redirect, render
# import ssl -> in case it doesn't work
import json
import mimetypes
import os
from django.http.response import HttpResponse
from wsgiref.util import FileWrapper
from home.models import Item

from shopify_app.views import new_session

from home.inventory_query import query_status, checking_status
from home.fetching import is_done, items_op, get_locations, bulk_operation, get_data, filter_data

# logging set-up
import logging
from django.conf import settings
fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.INFO)

logging.basicConfig(format=fmt, level=lvl)
logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))
'''
def new_session():
    # get session info
    shop_url = apps.get_app_config('shopify_app').SHOP_URL
    admin_api_key = apps.get_app_config('shopify_app').TOKEN
    api_version = apps.get_app_config('shopify_app').SHOPIFY_API_VERSION

    return shopify.Session(shop_url, api_version, admin_api_key)
'''

def index(request):
    # ssl._create_default_https_context = ssl._create_unverified_context

    

    items = Item.objects.all() 
    return render(request, 'home/incoming.html', {"items": items})


def update_page(request):
    # start session
#    client = new_session()
#    items = placeholder(client)
#    update_database(items)
    
    return redirect(index)
    items = Item.objects.all()
    return render(request, 'home/incoming.html', {"items": items }) 

   
def placeholder(client): # should i add request?
    # get locations using that get_locs function and passing session variable
    locs = get_locations()
    loc_id = " "
    # find the one that is 'Zedaro Office'
    for l in locs:
        if(l.attributes['name'] == 'Zedaro Head Office'):
            # get its id
            loc_id = l.attributes['admin_graphql_api_id']
    
    # create query hardcoding the location id in it
    if(loc_id != " "):
        while (is_done(client, checking_status) == False):
            sleep(10)
        inv_query = items_op(loc_id)
        logging.info(inv_query)
    # call the bulk_query
        bulk_query = bulk_operation(inv_query)
        logging.info(bulk_query)
        bulk = client.execute(bulk_query)
        logging.info(bulk)
    # call get_data (which gets the data once the status is COMPLETED)
        data = get_data(client, bulk, query_status)
        logging.info("got the data!!")
    # filter data?
        data = filter_data(data)
        logging.info(data)
    # generate excel file -> df to xlsx
          
        # update table       
    return data
    # generate html table
    #    html_table = get_html_table(data)
    #    logging.info(html_table)

    #return html_table

def get_item(s):
    try:
        found = Item.objects.get(sku=s)
        return found
    except Item.DoesNotExist:
        return False

def update_database(data):
    new_items = []
    for i,row in data.iterrows():
        item = get_item(row['SKU'])
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
    
    
            
def get_html_table(df):
    t = df.to_html(classes="table is-hoverable is-fullwidth")
    t_1 = t.replace('border="1" class="dataframe', 'class="')
    fixed_t = t_1.replace('<tr style="text-align: right;">', '<tr>')

    return fixed_t

# from "How To Download A File On Button Click in Django Easy STEPS" - YouTube · Askari BaDshah
# https://fedingo.com/how-to-download-file-in-django/
def download_file(request):
    # add way to change the file dynamically
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    file_name = 'test.xlsx'
    # Define the full file path
    filepath = BASE_DIR + '/home/Files/' + file_name
    file_name = os.path.basename(filepath)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(filepath, 'rb'), chunk_size), 
                                        content_type=mimetypes.guess_type(filepath)[0])
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = "Attachment;filename=%s" % file_name
    return response
