from time import sleep
from django.http import StreamingHttpResponse
from django.shortcuts import redirect, render
# import ssl -> in case it doesn't work
import json
import mimetypes
import os
from django.http.response import HttpResponse
from wsgiref.util import FileWrapper

import openpyxl
from home.models import Item, NumUpdated

from shopify_app.views import new_session

from home.inventory_query import query_status, checking_status
from home.fetching import is_done, items_op, get_locations, bulk_operation, get_data, filter_data
from home.updating import update_database, update_noi
#from django.utils import timezone
#from datetime import timedelta

import random

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
# Note: maybe either get all info, and only display what we want or do different requests you know?
def loading(request):
    n = NumUpdated.objects.first()
    if n is None:
        # set up default
        logging.info("no update found")
        return render(request, 'home/loading.html', {}) 
    else:
        return render(request, 'home/loading.html', {"date": n.updated_at})

def index(request):
    # ssl._create_default_https_context = ssl._create_unverified_context

    # get today's items 
    #today = timezone.now() - timedelta(days=1)
    #items = Item.objects.filter(updated_at__gte=today) 

    #one_hour_bef = timezone.now() - timedelta(hours=1)
    #items = Item.objects.filter(updated_at__gte=one_hour_bef).order_by('sku')
    n = NumUpdated.objects.first()
    if n is None:
        # set up default
        logging.info("no update found")
        return render(request, 'home/incoming.html', {}) 
    else:
        logging.info("last update found")
        items = Item.objects.filter(incoming__lte=0).order_by('-updated_at')[:n.items_updated]
        return render(request, 'home/incoming.html', {"items": items, "date": n.updated_at})


def update_page(request):
    # start session
    #client = new_session()
    #items = placeholder(client)
    
    #update_database(items)
    #sleep(60)
    update_noi(random.randint(5,20))

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
    
            
def get_html_table(df):
    t = df.to_html(classes="table is-hoverable is-fullwidth")
    t_1 = t.replace('border="1" class="dataframe', 'class="')
    fixed_t = t_1.replace('<tr style="text-align: right;">', '<tr>')

    return fixed_t

#def export_incoming(request):
#    export_excel(request, 'incoming')
# maybe add queryset object??

def export_excel(request):
    n = NumUpdated.objects.first()
    #if n is not None:

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="inventoryExport.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Inventory'

    # Write header row
    header = ['SKU', 'Available', 'Incoming']
    for col_num, column_title in enumerate(header, 1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.value = column_title

    # Write data rows
    queryset = Item.objects.order_by('-updated_at').filter(incoming__gt=0)[:n.items_updated].values_list('sku', 'available','incoming')
    
    for row_num, row in enumerate(queryset, 1):
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num+1, column=col_num)
            cell.value = cell_value

    workbook.save(response)

    return response

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
