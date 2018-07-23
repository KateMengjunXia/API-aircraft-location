Getting started:

Execute import.py to create a database and import initial data from the records.csv



API Usage:

Method: GET
URI: http://[hostname]/api/products
Parameters: page, per_page
Description: obtain the list of aircraft products. If page is specified, then number of products displayed on a page is per_page (default to be the total number of products)

Method: POST
URI: http://[hostname]/api/products
Content-Type: application/json
Description: add a new product

Method: GET
URI: http://[hostname]/api/products/<int:product_id>
Description: obtain information of the product specified by product_id

Method: PUT
URI: http://[hostname]/api/products/<int:product_id>
Content-Type: application/json
Description: update the product specified by product_id

Method: DELETE
URI: http://[hostname]/api/products/<int:product_id>
Description: delete the product specified by product_id

Method: GET
URI: http://[hostname]/api/products/<int:product_id>/locations
Parameters: page, per_page
Description: obtain the list of locations of the product specified by product_id. If page is specified, then number of products displayed on a page is per_page (default to be the total number of locations)

Method: POST
URI: http://[hostname]/api/products/<int:product_id>/locations
Content-Type: application/json
Description: add a new location to the product specified by product_id

Method: GET
URI: http://[hostname]/api/products/<int:product_id>/locations/<int:location_id
Description: obtain location specified by location_id (belongs to the product specified by product_id)

Method: PUT
URI: http://[hostname]/api/products/<int:product_id>/locations/<int:location_id
Content-Type: application/json
Description: update the location specified by location_id (belongs to the product specified by product_id)

Method: DELETE
URI: http://[hostname]/api/products/<int:product_id>/locations/<int:location_id
Description: delete the product specified by location_id (belongs to the product specified by product_id)



Note:

A interactive GUI can be viewed by accessing http://[hostname]
