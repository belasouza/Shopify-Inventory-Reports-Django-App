from django.shortcuts import render
import shopify
#from shopify_app.decorators import shop_login_required
import requests
from django.apps import apps
# import ssl -> in case it doesn't work
import json


#shop_login_required
def index(request):
    shop_url = apps.get_app_config('shopify_app').SHOP_URL
    admin_api_key = apps.get_app_config('shopify_app').TOKEN

    data_query = '''
    query {
        # Retrives the last 5 inventory items on a shop
        inventoryItems(first: 10, reverse:true) {
            edges {
            node {
                    id
                    tracked
                    sku
                }
            }
        }
    }
    '''

    # ssl._create_default_https_context = ssl._create_unverified_context
    #data = query_shopify(data_query, admin_api_key)
    shop_url = apps.get_app_config('shopify_app').SHOP_URL
    admin_api_key = apps.get_app_config('shopify_app').TOKEN
    api_version = apps.get_app_config('shopify_app').SHOPIFY_API_VERSION

    session = shopify.Session(shop_url, api_version, admin_api_key)
    shopify.ShopifyResource.activate_session(session)
    #items = shopify.GraphQL().execute(query=data_query)
    
    level = shopify.GraphQL().execute(query=inv_lev_query,
                                      variables={"item_id":"gid://shopify/InventoryLevel/107788927204?inventory_item_id=45622422700260"})
    #return render(result)
    #orders = shopify.Order.find(limit=3, order="created_at DESC")
    #products = shopify.Product.find(limit=5,order="created_at DESC")
    #return render(request, 'home/index.html', {'products':result})
    return render(request, 'home/yup.html', {'levels': level})

def query_shopify(query, admin_api_key):
    # headers that give access to the shop 
    
    headers = {
        'Content-Type': 'application/graphql',
        'X-Shopify-Access-Token': f'{admin_api_key}',
    }
    response = requests.post(f'https://zedaro.myshopify.com/admin/api/2023-04/graphql.json', data=query, headers=headers)
    #return response.json()