
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

inv_lev_query = '''
query ($item_id: ID!) {
    inventoryLevel(id:$item_id ) {
        id
        available
        incoming
        # The quantities field takes an array of inventory states, which include the following: "incoming", "on_hand", "available", "committed", and "reserved".
        quantities(names: ["available","incoming"]) {
          name
          quantity
        }
        item {
        id
        sku
        }
        location {
        id
        }
    }
}
'''

inv_item_query = '''
query($id: ID!, $loc: ID!) {
    inventoryItem(id: $id) {
        inventoryLevel(locationId: $loc){
            quantities(names: ["available","incoming"]) {
                name
                quantity
            }
        }
    }
}
'''