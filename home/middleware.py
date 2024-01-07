from django.apps import apps
from django.urls import reverse
import shopify

class ConfigurationError(BaseException):
    pass

class LoginProtection(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_key = apps.get_app_config('home').SHOPIFY_API_KEY
        self.api_secret = apps.get_app_config('home').SHOPIFY_API_SECRET
        if not self.api_key or not self.api_secret:
            raise ConfigurationError("SHOPIFY_API_KEY and SHOPIFY_API_SECRET must be set in ShopifyAppConfig")
        shopify.Session.setup(api_key=self.api_key, secret=self.api_secret)
        self.api_token = apps.get_app_config('home').TOKEN
        self.api_shop_url = apps.get_app_config('home').SHOP_URL
        if not self.api_token or not self.api_shop_url:
            raise ConfigurationError("TOKEN and SHOP_URL must be set in ShopifyAppConfig")
 
    def __call__(self, request):
        response = self.get_response(request)
        shopify.ShopifyResource.clear_session()
        return response

