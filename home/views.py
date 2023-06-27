from django.http import StreamingHttpResponse
from django.shortcuts import render
# import ssl -> in case it doesn't work
import json
import mimetypes
import os
from django.http.response import HttpResponse
from wsgiref.util import FileWrapper

from shopify_app.views import new_session

#from inventory_query import query_status, invItems_query
#from fetching import fetch_bulk, bulk_operation,bulk_status, get_data, filter_data

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

    # start session
    session, client = new_session()

    return render(request, 'home/index.html', {})
    
def placeholder(session, client): # should i add request?
    # get locations using that get_locs function and passing session variable

    # find the one that is 'Zedaro Office'
        # get its id
    
    # create query hardcoding the location id in it
    
    # call the bulk_query

    # call get_data (which gets the data once the status is COMPLETED)

    # filter data?

    # generate excel file
        # update file_name variable??? how???
        # 1) how to use cache
        # 2) how to clean cache?

    # generate html file
        # this one doesn't need to be a new one everytime i guess
    pass

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
