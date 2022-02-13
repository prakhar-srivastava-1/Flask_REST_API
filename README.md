# Flask_REST_API
A basic Flask REST API performing CRUD operations on a "cafe" application.

## API Documentation
GET
http://localhost:5000/all
<br>
Get all the cafes stored in the database.

GET
http://localhost:5000/random
<br>
Get a random cafefrom the database


GET http://localhost:5000/search
<br>
Usage http://localhost:5000/search?location=India
<br>
Query Params
location
India

POST http://localhost:5000/add
<br>
Pass the attributes as x-www-form-urlencoded to add a new Cafe 
Query Params
<br>name: string (Nullable=False)
<br>map_url: url
<br>img_url: url
<br>location: string
<br>seats: string
<br>has_toilet: bool ("True"/"true"/"1"/others => False)
<br>has_wifi: bool ("True"/"true"/"1"/others => False)
<br>has_sockets: bool ("True"/"true"/"1"/others => False)
<br>can_take_calls: bool ("True"/"true"/"1"/others => False)
<br>coffee_price: string

PATCH
http://localhost:5000/update-price/id?new_price=VALUE
<br>
Usage http://localhost:5000/update-price/23?new_price=INR 140
<br>Pick out the cafe using id and update the coffee price.
<br>Query Params
<br>new_price: string

DEL http://localhost:5000/report-closed/id?api-key=key
<br>Usage http://localhost:5000/report-closed/23?api-key=TopSecretAPIKey
<br>Delete the cafe with ID passed in URL. Validate API Key before deleting.
<br>Query Params
<br>api-key: TopSecretAPIKey