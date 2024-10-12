## How to run?:

 In outward and inward folder add your stripe API key since this is a private repo I am adding my stripe API Key
### Run the following command in terminal
```
$> docker compose up
```
### Hit the following URL
POST http://127.0.0.1:80/customers/

Content-Type: application/json

{
  "name": "xyz",
  "email": "xyz@mail.com"
}


## Project Structure

1. app folder - contains fastapi application and has POST /customers route to add a new customer to local postgres instance and also sends this to a queue

2. outward folder - contains a worker script that subscribes to "customer_updates" topic of kafka and pushes changes to stripe

3. inward folder - polls stripe api every 60 seconds to check for newly added customer, if the customer is not already there in our local postgres instance then adds them to postgres
