import sqlite3 as lite
import pandas as pd
import logging
#from django.conf import settings
#fmt = getattr(settings, 'LOG_FORMAT', None)
#lvl = getattr(settings, 'LOG_LEVEL', logging.INFO)

#ogging.basicConfig(format=fmt, level=lvl)

# function that creates new itemInfo table if needed
def new_table(cursor):
    tb_query = """CREATE TABLE IF NOT EXISTS itemInfo (
                  SKU VARCHAR(15),
                  Incoming INT,
                  Available INT );"""
    
    cursor.execute(tb_query)

# function to check if item is in database
def exists_item(cursor, sku):
    query = ("""SELECT SKU FROM itemInfo WHERE SKU = ?;""")
    cursor.execute(query, [(sku)])
    return cursor.fetchone() is not None

# function to insert item into the table
def insert_item(cursor, sku, available, incoming):
    query = ("""INSERT INTO itemInfo (SKU, Incoming, Available)
                VALUES(?,?,?);""")
    cursor.execute(query, (sku, incoming, available))

# function that updates the inventory levels
def update_levels(cursor, sku, available, incoming):
    query = ("""UPDATE itemInfo
                SET Incoming=?,
                    Available=?
                WHERE SKU=?;""")
    cursor.execute(query, (incoming, available, sku))

# function that updates the items already on the database 
# and adds the ones that aren't yet
def update_items(items):
    # connect to database
    con = lite.connect('inventoryInfo.db')
    # logging.info("Opened database")
    print("Opened database")

    # check if table exists
        # if not -> create table

    # cursor
    cur = con.cursor()
    
    new_items = []

    for i,row in items.iterrows():
        if exists_item(cur, row['SKU']):
            print("Updating...")
            update_levels(cur,row['Available'], row['Incoming'], row['SKU'])
        else: # need to add it to database
            # add to tmp df
            print("Item needs to be added")
            new_items.append(row)
    # commit changes
    #connection.commit() 
    
    if len(new_items) != 0: # if there are items to add
        for item in new_items:
            print("Adding...")
            insert_item(cur, item['SKU'], item['Available'], item['Incoming']) 
        #connection.commit()

    # HOW TO DELETE THE ONES THAT HAVEN'T BEEN UPDATED??
    # OR SUPPRESS THEM FROM SHOWING UP???
    con.close()
