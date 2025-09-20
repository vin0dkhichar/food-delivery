from app.core.kafka_consumer import consume_order_events

if __name__ == "__main__":
    print("Notification service started. Listening to Kafka events...")
    consume_order_events()
