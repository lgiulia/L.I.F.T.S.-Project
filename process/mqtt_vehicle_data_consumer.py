import paho.mqtt.client as mqtt
from config.mqtt_conf_params import MqttConfigurationParameters

def on_connect(client, userdata, flags, rc):
    # device_info_topic: /iot/user/<user_id>/device/+/info
    device_info_topic = "{0}/{1}/+/{2}".format(
        MqttConfigurationParameters.MQTT_BASIC_TOPIC,
        MqttConfigurationParameters.DEVICE_TOPIC,
        MqttConfigurationParameters.DEVICE_INFO_TOPIC
    )
    mqtt_client.subscribe(device_info_topic)
    print("Subscribed to: " + device_info_topic)

    # device_telemetry_topic: /iot/user/<user_id>/device/+/telemetry
    device_telemetry_topic = "{0}/{1}/+/{2}".format(
        MqttConfigurationParameters.MQTT_BASIC_TOPIC,
        MqttConfigurationParameters.DEVICE_TOPIC,
        MqttConfigurationParameters.DEVICE_TELEMETRY_TOPIC
    )
    mqtt_client.subscribe(device_telemetry_topic)

    print("Subscribed to: " + device_telemetry_topic)

def on_message(client, userdata, message):
    message_payload = str(message.payload.decode("utf-8")) # converte i dati binari in una stringa con la codifica UTF-8
    print(f"Received IoT Message: Topic: {message.topic} Payload: {message_payload}") # f": f string. Incorpora espressioni python all'interno di stringhe usando {}

device_id = "AGV-device-{0}".format(MqttConfigurationParameters.MQTT_USERNAME)
message_limit = 1000

mqtt_client = mqtt.Client(device_id)
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set(MqttConfigurationParameters.MQTTUSERNAME, MqttConfigurationParameters.MQTT_PASSWORD)

mqtt_client.connect(MqttConfigurationParameters.BROKER_ADDRESS, MqttConfigurationParameters.BROKER_PORT)
mqtt_client.loop_forever()