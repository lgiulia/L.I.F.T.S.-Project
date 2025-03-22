import paho.mqtt.client as mqtt
import time
from model.AGV_descriptor import AGVDescriptor
from model.AGV_TelemetryData import AGVTelemetryData
from config.mqtt_conf_params import MqttConfigurationParameters

def on_connect(client, userdata, flags, rc): # quando il client MQTT stabilisce una connessione con il broker
    print("Connected with result code " + str(rc))

def publish_telemetry_data():
    # telemetry topic: iot/user/<user_id>/device/<device_id>/telemetry
    target_topic = "{0}/{1}/{2}/{3}".format(
        MqttConfigurationParameters.MQTT_BASIC_TOPIC,
        MqttConfigurationParameters.DEVICE_TOPIC,
        device_id,
        MqttConfigurationParameters.DEVICE_TELEMETRY_TOPIC
    )
    device_payload_string = AGVTelemetryData.to_json()
    mqtt_client.publish(target_topic, device_payload_string, 0, False) # mqtt_client.publish(target_topic, device_payload_string, QoS (0), il broker non conserva il messaggio (False))
    print(f"Telemetry data Published: Topic: {target_topic} Payload: {device_payload_string}")

def publish_device_info():
    # device info topic: iot/user/<user_id>/device/<device_id>/info
    target_topic = "{0}/{1}/{2}/{3}".format(
        MqttConfigurationParameters.MQTT_BASIC_TOPIC,
        MqttConfigurationParameters.DEVICE_TOPIC,
        device_id,
        MqttConfigurationParameters.DEVICE_INFO_TOPIC
    )
    device_payload_string = AGVDescriptor.to_json()
    mqtt_client.publish(target_topic, device_payload_string, 0, True) # True: conserverà il messaggio
    print(f"Device Info Published: Topic: {target_topic} Payload: {device_payload_string}")

device_id = "AGV-vehicle-{0}".format(MqttConfigurationParameters.MQTT_USERNAME) # mettere un id univoco per ogni agv?
message_limit = 1000

mqtt_client = mqtt.Client(device_id)
mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set(MqttConfigurationParameters.MQTT_USERNAME, MqttConfigurationParameters.MQTT_PASSWORD)
mqtt_client.connect(MqttConfigurationParameters.BROKER_ADDRESS, MqttConfigurationParameters.BROKER_PORT)
mqtt_client.loop_start()

AGVDescriptor = AGVDescriptor(device_id, "KUKA", "alpha.01") # il prof mette anche username perchè ha guidatore ma a noi non serve?
AGVTelemetryData = AGVTelemetryData()

publish_device_info()

# Invio dopo 3 secondi dei nuovi dati di telemetria
for message_id in range(message_limit):
    AGVTelemetryData.update_measurements()
    publish_telemetry_data()
    time.sleep(3)

mqtt_client.loop_stop()