Inventory Reports Django App
==========================

This project makes it easy to check inventory and _export_ inventory levels as an Excel file from your Shopify shop.

It has the following structure:
- `home` (main app)
  - `authentication.py` sets up a Shopify API session and graphQL client
  - `fetching.py` handles the API calls
  - `updating.py` updates/creates the SQLite database
  - `importing.py` 
- `shopify_django_app` project files for serving this app.
### Demo
![](https://github.com/belasouza/Shopify-Inventory-Reports-Django-App/blob/main/demo.gif)

