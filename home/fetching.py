from time import sleep
import urllib.request
import pandas as pd
import json

def fetch_bulk(bulk_status):
    items = []
    # try block?
    if bulk_status['data']['node']['status']=='COMPLETED':
        url = bulk_status['data']['node']['url']
        inv_data = urllib.request.urlopen(url)
        for line in inv_data:
            line = json.loads(line.decode('utf8'))
            if 'sku' in line:
                items.append(line)
                print('Loading...')
    iframe=pd.DataFrame.from_records(items)
    return iframe

# from the other video
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

def bulk_status(client, bulk, status_query):
    bulk_id = json.loads(bulk)['data']['bulkOperationRunQuery']['bulkOperation']['id']
    status = json.loads(client.execute(status_query,{'id':bulk_id}))
    return status

def get_data(client, bulk):
    status = bulk_status(client,bulk)

    while(status['data']['node']['status']!='COMPLETED'):
        print("In Progress :)")
        sleep(15)
        status = bulk_status(client,bulk)

    # aka status is completed
    print(status)
    return fetch_bulk(status)

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
    df_a.columns = ['available']
    df_inc.columns = ['incoming']
    # get everything together
    df = pd.concat([data, df_a, df_inc], axis=1)
    # filter for the ones with incoming values
    df =  df[df.incoming != 0]
    # drop inventoryLevel column
    df = df.drop(['inventoryLevel'], axis=1)
    # reset index
    return df.reset_index(drop=True)
