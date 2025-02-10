import pika
import json

def simple_model(features):
    # Simple mock model that returns sum of features
    return sum(features)

def callback(ch, method, properties, body):
    message = json.loads(body)
    features = message['body']
    
    # Generate prediction
    prediction = simple_model(features)
    
    # Create prediction message
    pred_message = {
        'id': message['id'],
        'body': prediction
    }
    
    # Send prediction to y_pred queue
    ch.basic_publish(
        exchange='',
        routing_key='y_pred',
        body=json.dumps(pred_message)
    )
    print(f"Sent prediction for id: {message['id']}")

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
        port=5672,
        connection_attempts=3,
        retry_delay=5
    ))
    channel = connection.channel()

    # Declare queues
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_pred')

    # Set up consumer
    channel.basic_consume(
        queue='features',
        on_message_callback=callback,
        auto_ack=True
    )

    print("Model service is waiting for features...")
    channel.start_consuming()
except pika.exceptions.AMQPConnectionError:
    print("Error connecting to RabbitMQ. Please ensure:")
    print("1. RabbitMQ is installed")
    print("2. RabbitMQ server is running (brew services start rabbitmq)")
    print("3. Server is available at localhost:5672")
    exit(1)