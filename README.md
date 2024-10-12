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

1. App folder - This component handles customer creation via a POST /customers endpoint. When a customer is created, it pushes an event to a kafka.

2. Outward folder - This worker subscribes to "customer_updates" topic in kafka, processes the events, and updates the customer data in Stripe.

3. Inward folder - This component polls the Stripe API every 60 seconds to check for updates and syncs the data back to your local PostgreSQL database

4. Currently the application only handles creations of new user but if we modify database schema to have last_updated_time and created_time, we can also handle updates and deletions


## Salesforce integration:
- Develop a new worker (consumer group) that also subscribes to "customer_updates" topic in kafka and manages data interactions with the Salesforce API. 
- Batch Processing: Implement batch processing for handling multiple updates at once, reducing the number of API calls to Salesforce and improving efficiency.

## Extension to Invoice catalog
- Can create a new POST /invoice route to add invoice to our database
- Will also need to create new topics, since Kafka has high throughput it will be scalable
- Instead of modifying existing (customer catalog) workers, create separate invoice workers that can handle events. This maintains separation of responsibilities.
