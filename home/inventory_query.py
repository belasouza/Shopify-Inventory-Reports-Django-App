query_status = """
query bulkStatus($id:ID!){
  node(id: $id) {
    ... on BulkOperation {
      id
      status
      errorCode
      createdAt
      completedAt
      objectCount
      fileSize
      url
      partialDataUrl
    }
  }
}
"""

#actually will need to use gql module to add the locationId correctly !!
invItems_query = """
{
    inventoryItems {
    edges {
        node {
        sku
        inventoryLevel(locationId:"gid://shopify/Location/36462395441"){
            quantities(names: ["available","incoming"]) {
              name
              quantity
            }
        }
        }
    }
    }
}
"""

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

individual_inv_levels = '''
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