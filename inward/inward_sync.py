import time
import schedule
import stripe
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL="postgresql://postgres:password@postgres:5432/mydb"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)

Base.metadata.create_all(engine)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stripe.api_key = "sk_test_51Q8qNR03SnHpXEcqOqdTZpCnl1us65bFQ4EIwfY5xUXrnB5Oj73WVWWV6ujTd3IwZTIowOFs76olCp95AS3yTKD40022hVRFEc"

# producer = KafkaProducer(
#     bootstrap_servers=['kafka:9092'],
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# Kafka topic for customer updates
# KAFKA_TOPIC = "stripe_updates"

# def send_to_kafka(topic, data):
    # try:
    #     future = producer.send(topic, data)
    #     record_metadata = future.get(timeout=10)
    #     logger.info(
    #         f"Sent message to Kafka topic {topic}, partition {record_metadata.partition}, offset {record_metadata.offset}")
    # except KafkaError as e:
    #     logger.error(f"Failed to send message to Kafka: {str(e)}")

def fetch_stripe_updates():
    session = Session()
    try:
        one_min_ago = int((datetime.utcnow() - timedelta(seconds=60)).timestamp())
        updated_customers = stripe.Customer.list(created={'gte': one_min_ago})

        for stripe_customer in updated_customers.auto_paging_iter():
            local_customer = session.query(Customer).filter_by(
                email=stripe_customer.email,
                name=stripe_customer.name
            ).first()

            if local_customer:
                logger.info(f"Skipping customer {stripe_customer.id}: email and name combination already exists")
                continue

            # customer_data = {
            #     'id': stripe_customer.id,
            #     'email': stripe_customer.email,
            #     'name': stripe_customer.name,
            # }
            # send_to_kafka(KAFKA_TOPIC, customer_data)
            logger.info(f"Processed new customer: {stripe_customer.id}")

            # Create new customer in local database
            new_customer = Customer(
                # id=stripe_customer.id,
                email=stripe_customer.email,
                name=stripe_customer.name
            )
            session.add(new_customer)

        session.commit()
        logger.info("Stripe inward sync completed.")

    except stripe.error.StripeError as e:
        logger.error(f"Stripe API error: {str(e)}")
        session.rollback()
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        session.rollback()
    finally:
        session.close()


def run_sync():
    logger.info("Running Stripe inward sync...")
    fetch_stripe_updates()

schedule.every(60).seconds.do(run_sync)

if __name__ == "__main__":
    logger.info("Starting Stripe inward sync service...")
    while True:
        schedule.run_pending()
        time.sleep(1)