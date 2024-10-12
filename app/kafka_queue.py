from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Kafka producer with error handling and retry mechanism
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    retries=5,
    retry_backoff_ms=1000,
    acks='all'
)

KAFKA_TOPIC = "customer_updates"

def send_to_queue(topic, data):
    try:
        future = producer.send(topic, data.encode('utf-8'))
        record_metadata = future.get(timeout=10)
        logger.info(f"Message sent successfully to topic {topic} at partition {record_metadata.partition} with offset {record_metadata.offset}")
    except KafkaError as e:
        logger.error(f"Failed to send message to Kafka: {str(e)}")