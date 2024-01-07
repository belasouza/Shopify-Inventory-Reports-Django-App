from django.apps import apps
import shopify

def new_session():
    '''
    returns session and graphql client
    '''

    # get store details
    shop_url = apps.get_app_config('home').SHOP_URL
    admin_api_key = apps.get_app_config('home').TOKEN 
    api_version = apps.get_app_config('home').SHOPIFY_API_VERSION
    api_key = apps.get_app_config('home').SHOPIFY_API_KEY 
    api_secret = apps.get_app_config('home').SHOPIFY_API_SECRET
    
    # set up and create session
    shopify.Session.setup(api_key=api_key, secret=api_secret)
    session = shopify.Session(shop_url, api_version, admin_api_key)

    # start session
    shopify.ShopifyResource.activate_session(session)
    
    # get graphql client
    client = shopify.GraphQL()
    return client
