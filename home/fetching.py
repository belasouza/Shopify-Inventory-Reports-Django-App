from time import sleep
import urllib.request
import pandas as pd
import json
import shopify
import logging
from django.conf import settings
from home.inventory_query import query_status 

fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.INFO)

logging.basicConfig(format=fmt, level=lvl)

def get_locations():
  all_locs = []
  page = shopify.Location.find(since_id=0, limit=250)
  for loc in page:
    all_locs.append(loc)
  while page.has_next_page():
      page=page.next_page()
      for loc in page:
        all_locs.append(loc)
  return all_locs

def items_op(loc_id):
    query = '{ inventoryItems { edges { node { sku inventoryLevel(locationId:"' + loc_id + '"){ quantities(names:["available","incoming"]) { name quantity } } } } } }'
    return query

def bulk_operation(query):
    bulk_query="""
        mutation {{
            bulkOperationRunQuery(
            query:\"""{query}\"""
            ) {{
                bulkOperation {{
                    id
                    status
                }}
                userErrors {{
                    field 
                    message
                }}
            }}
        }}
    """.format(query=query)
    return bulk_query

def get_data(client, bulk, sq):
    status = bulk_status(client,bulk, sq)

    while(status['data']['node']['status']!='COMPLETED'):
        logging.info("In Progress :)")
        sleep(15)
        status = bulk_status(client,bulk, sq)

    # aka status is completed
    logging.info(status)
    return fetch_bulk(status)

def bulk_status(client, bulk, status_query):
    bulk_id = json.loads(bulk)['data']['bulkOperationRunQuery']['bulkOperation']['id']
    status = json.loads(client.execute(status_query,{'id':bulk_id}))
    return status

def fetch_bulk(bulk_status):
    items = []
    # try block?
    if bulk_status['data']['node']['status']=='COMPLETED':
        url = bulk_status['data']['node']['url']
        inv_data = urllib.request.urlopen(url)
        for line in inv_data:
            line = json.loads(line.decode('utf8'))
            # if there are at least one item incoming... -> CHANGE THIS TO ADD ALL ITEMS, then on query we will filter it
            # maybe change it to line['inventoryLevel']['quantities'][0]['quantity'] != 0 -> incoming is not 0
            # ORRR change fetch bulk according to request, add other variable like if incoming, do this, if available do that ??
            logging.info(line)
            if line['inventoryLevel'] != None:
                #if line['inventoryLevel']['quantities'][1]['quantity'] > 0:
                items.append(line) # get line
                logging.info('Loading...')
    iframe=pd.DataFrame.from_records(items)
    return iframe
    
def filter_data(data):
    # get quantities column
    df = pd.json_normalize(data['inventoryLevel'])
    
    # flatten pd.quantities
    df_q = df['quantities'].apply(pd.Series)
    
    # get each level
    df_a = df_q[0].apply(pd.Series)
    df_inc = df_q[1].apply(pd.Series)
    
    # drop name column
    df_a = df_a.drop(['name'], axis=1)
    df_inc = df_inc.drop(['name'], axis=1)
    
    # rename columns
    df_a.columns = ['Available']
    df_inc.columns = ['Incoming']
    
    # get everything together
    df = pd.concat([data, df_a, df_inc], axis=1)

    # drop inventoryLevel column
    df = df.drop(['inventoryLevel'], axis=1)

    # reset index
    df.reset_index(drop=True, inplace=True)

    # rename column
    return df.rename(columns={"sku":"SKU"})

def fetching_manager(client): 
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