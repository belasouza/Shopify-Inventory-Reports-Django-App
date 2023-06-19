from django.shortcuts import render
import shopify
#from shopify_app.decorators import shop_login_required
import requests
from django.apps import apps
# import ssl -> in case it doesn't work
import json
from inventory_query import inv_lev_query, inv_item_query

def new_session():
    # get session info
    shop_url = apps.get_app_config('shopify_app').SHOP_URL
    admin_api_key = apps.get_app_config('shopify_app').TOKEN
    api_version = apps.get_app_config('shopify_app').SHOPIFY_API_VERSION

    return shopify.Session(shop_url, api_version, admin_api_key)

def get_products():
    all_products = []
    attribute=getattr(shopify,object_name)
    data=attribute.find(since_id=0,limit=250)
    for d in data:
        all_products.append(d)
    while data.has_next_page():
        data=data.next_page()
        for d in data:
            all_products.append(d)
        return all_products

#shop_login_required
def index(request):
    # ssl._create_default_https_context = ssl._create_unverified_context

    # start session
    session = new_session()
    shopify.ShopifyResource.activate_session(session)

    #level = shopify.GraphQL().execute(query=inv_lev_query, variables={"item_id":"gid://shopify/InventoryLevel/107788927204?inventory_item_id=45622422700260"})
    
    #products = shopify.Product.find(limit=5,order="created_at DESC")
    return render(request, 'home/index.html', {})
    #return render(request, 'home/yup.html', {'items':items, 'levels': level})
    
def query_shopify(query, admin_api_key):
    # headers that give access to the shop 
    
    headers = {
        'Content-Type': 'application/graphql',
        'X-Shopify-Access-Token': f'{admin_api_key}',
    }
    response = requests.post(f'https://zedaro.myshopify.com/admin/api/2023-04/graphql.json', data=query, headers=headers)
    #return response.json()