import pika
import time
import json
import random
from datetime import datetime

import os

# Тестовые данные
features = [
    [0.1, 0.2, 0.3],
    [0.4, 0.5, 0.6],
    [0.7, 0.8, 0.9]
]
y_true = [100, 200, 300]  # Cписок "истинных" ответов

# Устанавливаем соединение с RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'localhost'),
        port=5672,
        connection_attempts=3,
        retry_delay=5
    ))
    channel = connection.channel()

    # Объявляем очереди
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred') 
    channel.queue_declare(queue='features')

    print("Запуск сервиса. Отправка сообщений...")
except pika.exceptions.AMQPConnectionError:
    print("Ошибка подключения к RabbitMQ. Пожалуйста, убедитесь, что:")
    print("1. RabbitMQ установлен")
    print("2. RabbitMQ сервер запущен (brew services start rabbitmq)")
    print("3. Сервер доступен на localhost:5672")
    exit(1)

while True:
    # Генерируем уникальный идентификатор на основе текущего времени
    message_id = datetime.timestamp(datetime.now())
    
    # Выбираем случайное наблюдение
    idx = random.randint(0, len(y_true) - 1)
    
    # Формируем сообщения с общим идентификатором
    message_y_true = {
        'id': message_id,
        'body': y_true[idx]
    }
    message_features = {
        'id': message_id,
        'body': features[idx]
    }
    
    # Отправляем сообщения в соответствующие очереди
    channel.basic_publish(exchange='', routing_key='y_true', body=json.dumps(message_y_true))
    channel.basic_publish(exchange='', routing_key='features', body=json.dumps(message_features))
    
    print(f"Отправлены сообщения с id: {message_id}")
    
    # Задержка перед следующей итерацией
    time.sleep(5)