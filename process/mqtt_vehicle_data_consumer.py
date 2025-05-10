import paho.mqtt.client as mqtt
from config.mqtt_conf_params import MqttConfigurationParameters
import json
import requests

HTTP_ENDPOINT_URL = "http://127.0.0.1:7070/api/iot/inventory/AGV"
MQTT_DEVICE_TOPIC_SEGMENT = MqttConfigurationParameters.DEVICE_TOPIC

def on_connect(client, userdata, flags, rc):
    # device_info_topic: /iot/user/<user_id>/device/+/info
    device_info_topic = "{0}/{1}/+/{2}".format(
        MqttConfigurationParameters.MQTT_BASIC_TOPIC,
        MQTT_DEVICE_TOPIC_SEGMENT,
        MqttConfigurationParameters.DEVICE_INFO_TOPIC
    )
    mqtt_client.subscribe(device_info_topic)
    print("Subscribed to: " + device_info_topic)

    # device_telemetry_topic: /iot/user/<user_id>/device/+/telemetry
    device_telemetry_topic = "{0}/{1}/+/{2}".format(
        MqttConfigurationParameters.MQTT_BASIC_TOPIC,
        MQTT_DEVICE_TOPIC_SEGMENT,
        MqttConfigurationParameters.DEVICE_TELEMETRY_TOPIC
    )
    mqtt_client.subscribe(device_telemetry_topic)

    print("Subscribed to: " + device_telemetry_topic)

def on_message(client, userdata, message):
    print(f"Received IoT Message: Topic: {message.topic} Payload: {message.payload.decode()}") # f": f string. Incorpora espressioni python all'interno di stringhe usando {}
    try:
        senml_data = json.loads(message.payload.decode('utf-8'))
        print("Parsed SenML data:", senml_data)

        # Estrai l'ID del dispositivo dal topic MQTT
        topic_parts = message.topic.split('/')
        device_id_index = topic_parts.index(MQTT_DEVICE_TOPIC_SEGMENT) + 1
        if device_id_index < len(topic_parts) and topic_parts[device_id_index]:
            agv_id = topic_parts[device_id_index]
            http_endpoint_url = f"{HTTP_ENDPOINT_URL}/{agv_id}/mqtt_data"  # URL specifico per l'AGV

        #Invia i dati SenML via HTTP POST
        headers = {'Content-Type': 'application/senml+json'}
        try:
            response = requests.post(http_endpoint_url, headers=headers, json=senml_data)
            response.raise_for_status() #Solleva un'eccezione per codici di stato HTTP errati
            print(f"SenML data sent via HTTP. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending HTTP request: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON payload: {e}")

device_id = "AGV-device-{0}".format(MqttConfigurationParameters.MQTT_USERNAME)
message_limit = 1000

mqtt_client = mqtt.Client(device_id)
mqtt_client.subscribe(f"{MqttConfigurationParameters.MQTT_BASIC_TOPIC}/{MqttConfigurationParameters.DEVICE_TOPIC}/#", 0)
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set(MqttConfigurationParameters.MQTT_USERNAME, MqttConfigurationParameters.MQTT_PASSWORD)

mqtt_client.connect(MqttConfigurationParameters.BROKER_ADDRESS, MqttConfigurationParameters.BROKER_PORT)
mqtt_client.loop_forever()