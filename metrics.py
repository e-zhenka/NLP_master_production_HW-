import pika
import json
import csv
import os

CSV_FILE = os.getenv('CSV_FILE', '/app/logs/metric_log.csv')

# Create CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'y_true', 'y_pred', 'absolute_error'])

messages = {}

def process_message(msg_type, message):
    msg_id = message['id']
    value = message['body']
    
    if msg_id not in messages:
        messages[msg_id] = {}
    messages[msg_id][msg_type] = value
    
    # If both y_true and y_pred are available, calculate error and log
    if 'y_true' in messages[msg_id] and 'y_pred' in messages[msg_id]:
        y_true_val = messages[msg_id]['y_true']
        y_pred_val = messages[msg_id]['y_pred']
        absolute_error = abs(y_true_val - y_pred_val)
        
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([msg_id, y_true_val, y_pred_val, absolute_error])
        
        print(f"Logged metric for id {msg_id} with error: {absolute_error}")
        del messages[msg_id]

def callback_y_true(ch, method, properties, body):
    message = json.loads(body)
    process_message('y_true', message)
    
def callback_y_pred(ch, method, properties, body):
    message = json.loads(body)
    process_message('y_pred', message)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='y_true')
channel.queue_declare(queue='y_pred')

channel.basic_consume(queue='y_true', on_message_callback=callback_y_true, auto_ack=True)
channel.basic_consume(queue='y_pred', on_message_callback=callback_y_pred, auto_ack=True)

print("Metric service is waiting for messages...")
channel.start_consuming()