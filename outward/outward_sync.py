from kafka import KafkaConsumer
import stripe

stripe.api_key = "sk_test_51Q8qNR03SnHpXEcqOqdTZpCnl1us65bFQ4EIwfY5xUXrnB5Oj73WVWWV6ujTd3IwZTIowOFs76olCp95AS3yTKD40022hVRFEc"

consumer = KafkaConsumer('customer_updates', bootstrap_servers='kafka:9092')

def stripe_sync_worker():
    for message in consumer:
        customer_data = message.value.decode('utf-8').split(',')
        stripe.Customer.create(
            name=customer_data[1],
            email=customer_data[2]
        )

if __name__ == "__main__":
    stripe_sync_worker()
