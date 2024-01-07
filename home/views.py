from django.http import StreamingHttpResponse
from django.shortcuts import redirect, render, reverse
import mimetypes
import os
from django.http.response import HttpResponse
from wsgiref.util import FileWrapper

import openpyxl
from home.models import Item, Update

from home.authentication import new_session
from home.fetching import fetching_manager
from home.updating import update_database



# logging set-up
import logging
from django.conf import settings
fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.INFO)

logging.basicConfig(format=fmt, level=lvl)
logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))

# helper functions
# views
def index(request):
    return render(request, 'home/homepage.html') 

def all_items(request):
    u = Update.objects.first()
    if u is None:
        # set up default
        logging.info("no update found")
        return render(request, 'home/all_items.html', {}) 
    else:
        logging.info("last update found")
        items = Item.objects.order_by('sku')
        return render(request, 'home/all_items.html', {"items": items, "date": u.updated_at})

def out_stock(request):
    u = Update.objects.first()
    if u is None:
        # set up default
        logging.info("no update found")
        return render(request, 'home/outstock.html', {}) 
    else:
        logging.info("last update found")
        items = Item.objects.filter(available__lte=0).order_by('sku')
        return render(request, 'home/outstock.html', {"items": items, "date": u.updated_at}) 
    
def incoming(request):
    u = Update.objects.first()
    if u is None:
        # set up default
        logging.info("no update found")
        return render(request, 'home/incoming.html', {}) 
    else:
        logging.info("last update found")
        items = Item.objects.filter(incoming__gt=0).order_by('sku')
        return render(request, 'home/incoming.html', {"items": items, "date": u.updated_at})

def update_page(request, page=""):
    page = request.GET.get('page')
    
    logging.info("updating")
    # start session
    client = new_session()
        
    items = fetching_manager(client)
        
    update_database(items)
        
    items = Item.objects.all()
    
    if page == "all":
        logging.info('all items')
        return redirect(all_items)
    elif page == "incoming":
        logging.info('incoming')
        return redirect(incoming) 
    elif page == "out":
        logging.info('incoming')
        return redirect(out_stock)
    else:   
        return redirect(index) 

"""
def get_data(client): 
    # get locations using that get_locs function and passing session variable
    locs = get_locations()
    loc_id = " "
    # find the one that is 'Main Location'
    for l in locs:
        logging.info(l)
        if(l.attributes['name'] == 'Main Location'):
            # get its id
            logging.info('get its id')
            loc_id = l.attributes['admin_graphql_api_id']
            logging.info(loc_id)
            
        # create query hardcoding the location id in it
        if(loc_id != " "):
            #while (is_done(client, checking_status) == False):
            #    sleep(10)
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
"""
  
def export_excel(request):
    u = Update.objects.first()
    if u is not None:

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
        prev = request.META.get('HTTP_REFERER')
        if "incoming" in prev:
            queryset = Item.objects.order_by('sku').filter(incoming__gt=0).values_list('sku', 'available','incoming')
        elif "out_of_stock" in prev:
            queryset = Item.objects.order_by('sku').filter(available__lte=0).values_list('sku', 'available','incoming') 
        else: 
            queryset = Item.objects.order_by('sku').values_list('sku', 'available','incoming') 
        
        for row_num, row in enumerate(queryset, 1):
            for col_num, cell_value in enumerate(row, 1):
                cell = worksheet.cell(row=row_num+1, column=col_num)
                cell.value = cell_value

        workbook.save(response)

        return response
    else:
        return redirect(index)


# from "How To Download A File On Button Click in Django Easy STEPS" - YouTube · Askari BaDshah
# https://fedingo.com/how-to-download-file-in-django/
def download_file(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    file_name = 'inventory_report.xlsx'
    # Define the full file path
    filepath = BASE_DIR + '/home/Files/' + file_name
    file_name = os.path.basename(filepath)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(filepath, 'rb'), chunk_size), 
                                        content_type=mimetypes.guess_type(filepath)[0])
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = "Attachment;filename=%s" % file_name
    return response
