import time
import schedule
import stripe
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL="postgresql://postgres:password@postgres:5432/mydb"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)

Base.metadata.create_all(engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stripe.api_key = "sk_test_51Q8qNR03SnHpXEcqOqdTZpCnl1us65bFQ4EIwfY5xUXrnB5Oj73WVWWV6ujTd3IwZTIowOFs76olCp95AS3yTKD40022hVRFEc"

def fetch_stripe_updates():
    session = Session()
    try:
        one_min_ago = int((datetime.now(timezone.utc) - timedelta(seconds=60)).timestamp())
        updated_customers = stripe.Customer.list(created={'gte': one_min_ago})

        for stripe_customer in updated_customers.auto_paging_iter():
            local_customer = session.query(Customer).filter_by(
                email=stripe_customer.email,
                name=stripe_customer.name
            ).first()

            if local_customer:
                logger.info(f"Skipping customer {stripe_customer.id}: email and name combination already exists")
                continue

            logger.info(f"Processed new customer: {stripe_customer.id}")

            new_customer = Customer(name=stripe_customer.name, email=stripe_customer.email)
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