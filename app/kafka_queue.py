from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: v.encode('utf-8'),
    retries=5,
    retry_backoff_ms=1000,
    acks='all'
)

KAFKA_TOPIC = "customer_updates"

def send_to_queue(topic, data):
    try:
        future = producer.send(topic, data)
        record_metadata = future.get(timeout=10)
        logger.info(f"Message sent successfully to topic {topic} at partition {record_metadata.partition} with offset {record_metadata.offset}")
    except KafkaError as e:
        logger.error(f"Failed to send message to Kafka: {str(e)}")
