import sqlite3 as lite

# new_table creates new itemInfo table if needed
def new_table(cursor):
    tb_query = """CREATE TABLE IF NOT EXISTS itemInfo (
                  SKU VARCHAR(15),
                  Incoming INT,
                  Available INT );"""
    
    cursor.execute(tb_query)

# exists_item checks if item is in database
def exists_item(cursor, sku):
    query = ("""SELECT SKU FROM itemInfo WHERE SKU = ?;""")
    cursor.execute(query, [(sku)])
    return cursor.fetchone() is not None

# insert_items inserts item into the table
def insert_item(cursor, sku, available, incoming):
    query = ("""INSERT INTO itemInfo (SKU, Incoming, Available)
                VALUES(?,?,?);""")
    cursor.execute(query, (sku, incoming, available))

# update_levels updates the inventory levels
def update_levels(cursor, sku, available, incoming):
    query = ("""UPDATE itemInfo
                SET Incoming=?,
                    Available=?
                WHERE SKU=?;""")
    cursor.execute(query, (incoming, available, sku))

# update_items updates the items already on the database 
# and adds the ones that aren't yet
def update_items(items):
    # connect to database
    con = lite.connect('inventoryInfo.db')

    # cursor
    cur = con.cursor()
    
    new_items = []

    for i,row in items.iterrows():
        if exists_item(cur, row['SKU']):
            update_levels(cur,row['Available'], row['Incoming'], row['SKU'])
        else: # need to add it to database
            # add to tmp df
            new_items.append(row)
    
    if len(new_items) != 0: # if there are items to add
        for item in new_items:
            insert_item(cur, item['SKU'], item['Available'], item['Incoming']) 

    con.close()
