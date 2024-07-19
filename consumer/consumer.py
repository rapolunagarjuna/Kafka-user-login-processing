from collections import defaultdict
import json
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime


"""
We are maintaining a in-memory db to calculate the statistics of the user logins.
In a production environment, we would use a database to store the data and calculate the statistics.
In a production environment, we would also use a distributed system like Apache Flink to process the data in real-time.

For now, we are using a simple in-memory db to calculate the statistics.
We are using a dict to store the data.
Some of the statistics we are calculating are:
- Average devices per user
- Min devices per user
- Max devices per user
- Different device types
- Different locations
- Logins at night
- Logins in the morning
"""
per_user_login_count = defaultdict(int)
logins_per_device_type_count = defaultdict(int)
logins_per_location = defaultdict(int)
logins_by_hour = defaultdict(int) 

"""
We are sanitizing the input message to check if it has all the required fields.
The required fields are:
- user_id
- device_type
- device_id
- locale
- timestamp

If the message has all the required fields, we return True, else we return False.
"""
def is_valid_message(message):
    required_fields = ["user_id", "device_type", "device_id", "locale", "timestamp"]
    return all(field in message for field in required_fields)
 
"""
We are processing the message to calculate the statistics.
We are updating the following statistics:
- Device counts per user
- Device type counts
- Location counts
- Logins by hour
"""
def process_message(message):
    user_id = message.get("user_id")
    device_type = message.get("device_type")
    locale = message.get("locale")
    timestamp = message.get("timestamp")

    dt = datetime.fromtimestamp(timestamp)
    hour_of_day = dt.hour

    per_user_login_count[user_id] += 1
    logins_per_device_type_count[device_type] += 1
    logins_per_location[locale] += 1
    logins_by_hour[hour_of_day] += 1

def calculate_statistics():
    total_logins = sum(per_user_login_count.values())
    average_logins = total_logins / len(per_user_login_count) if per_user_login_count else 0
    min_logins = min(per_user_login_count.values()) if per_user_login_count else 0
    max_logins = max(per_user_login_count.values()) if per_user_login_count else 0
    
    different_device_types = len(logins_per_device_type_count)
    different_locations = len(logins_per_location)
    
    logins_at_night = sum(count for hour, count in logins_by_hour.items() if 0 <= hour < 6)
    logins_in_morning = sum(count for hour, count in logins_by_hour.items() if 6 <= hour < 12)

    return average_logins, min_logins, max_logins, different_device_types, different_locations, logins_at_night, logins_in_morning

"""
for debugging purposes
"""
def on_send_success(record_metadata):
    print(f"Message sent to topic {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")

def on_send_error(excp):
    print('Error sending message', exc_info=excp)

def main():
    bootstrap_servers = 'kafka:9092'
    input_topic = 'user-login'
    stats_topic = 'user-device-stats'

    consumer = KafkaConsumer(
        input_topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    for msg in consumer:
        print("Consumed message: ", msg.value)
        message = msg.value
        if is_valid_message(message):
            process_message(message)
            
            average_logins, min_logins, max_logins, different_device_types, different_locations, logins_at_night, logins_in_morning = calculate_statistics()

            stats_message = {
                "average_logins_per_user": average_logins,
                "min_logins_per_user": min_logins,
                "max_logins_per_user": max_logins,
                "different_device_types": different_device_types,
                "different_locations": different_locations,
                "logins_at_night": logins_at_night,
                "logins_in_morning": logins_in_morning,
                "user_login_per_device_type": dict(logins_per_device_type_count),
                "user_login_per_location": dict(logins_per_location), 
            }

            print("Stats: ", stats_message)

            producer.send(stats_topic, value=stats_message)
            producer.flush()

    consumer.close()
    producer.close()

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(e)
