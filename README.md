Inventory Reports Django App
==========================

This project makes it easy to export Excel files from Shopify inventory. 

This project has the following structure
- `home` (main app)
  - `authentication.py` sets up a Shopify API session and graphQL client
  - `fetching.py` handles the API calls and stores the responses in a Python data frame
  - `updating.py` updates/creates the SQLite database using the data frame from 'fetching.py'
- `shopify_django_app` project files for serving this app.

Get It Running
--------------

### Create Your App Configuration
- Log in to your [partners dashboard](https://partners.shopify.com/)
- Navigate to [your apps](https://partners.shopify.com/current/apps)
- Click `Create App`
- Choose a custom app
- Fill in the app name

- Log in to your test store
- Navigate to Settings
- Click `Create Custom App`
- Update API scope
- Get the app token 

You will then have access to your admin token, API key and API secret KEY, you will need these
for the next steps.

### Setup Environment

1. Copy over the `.env.local` file into a `.env` file and fill out the `SHOPIFY_API_KEY`, `SHOPIFY_API_SECRET`, `TOKEN`, `SHOP_URL` and `SHOPIFY_API_VERSION` fields
  * `SHOP_URL` is in the form of `https://<STORENAME>.myshopify.com/admin/api/<API VERSION>`
  * `SHOPIFY_API_VERSION` is one of `2024-01, 2023-10, 2023-07, 2023-04, 2023-01, 2022-10, 2022-07, 2022-04, 2022-01`
```
cp .env.local .env
```

2. Generate a secret key and add it to `.env` by running the following in the command line: 

```
python -c 'import random; print("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]))' >> .env
```

**For PC Users:** Run this command in [GIT Bash](https://git-scm.com/) or [Windows Subsystem For Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). Alternatively, you can generate a secret key using the Python interpreter. This requires you to manually add the Django secret key to your `.env` file by doing the following:

Open the python interpreter:
```
python
```
Inside the python interpreter, generate the secret key, copy it, and exit:
```python
>>> import random
>>> print("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]))
>>> exit()
```


### Run the App

  1. With the `.env` already created in the root directory, build the docker image:

  ```
  docker-compose build
  ```
  
  2. Run the container:
  ```
  docker-compose up
  ```

Open <http://localhost:8000> in your browser to view the example.
