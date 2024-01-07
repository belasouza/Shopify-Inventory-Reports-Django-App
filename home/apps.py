from django.apps import AppConfig
import os

class HomeConfig(AppConfig):
    name = 'home'

    # Replace the API Key and Shared Secret with the one given for your
    # App by Shopify'
    #
    # To create an application, or find the API Key and Secret, visit:
    # - for private Apps:
    #     https://${YOUR_SHOP_NAME}.myshopify.com/admin/api
    # - for partner Apps:
    #     https://www.shopify.com/services/partners/api_clients
    #
    # You can ignore this file in git using the following command:
    #   git update-index --assume-unchanged shopify_settings.py
    SHOP_URL = os.environ.get('SHOP_URL')
    TOKEN = os.environ.get('TOKEN')

    # API_VERSION specifies which api version that the app will communicate with
    SHOPIFY_API_VERSION = os.environ.get('SHOPIFY_API_VERSION')

    # See http://api.shopify.com/authentication.html for available scopes
    # to determine the permissions your app will need.
    SHOPIFY_API_SCOPE = os.environ.get('SHOPIFY_API_SCOPE', 'read_products,read_orders').split(',')

    SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY')
    SHOPIFY_API_SECRET = os.environ.get('SHOPIFY_API_SECRET')