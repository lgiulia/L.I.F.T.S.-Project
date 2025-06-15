import paho.mqtt.client as mqtt
import time
from model.AGV_descriptor import AGVDescriptor
from model.AGV_TelemetryData import AGVTelemetryData
from config.mqtt_conf_params import MqttConfigurationParameters
import json

def on_connect(client, userdata, flags, rc): # quando il client MQTT stabilisce una connessione con il broker
    print("Connected with result code " + str(rc))

def publish_telemetry_data(agv_data, telemetry_data):
    # telemetry topic: iot/user/<user_id>/device/<device_id>/telemetry
    target_topic = "{0}/{1}/{2}/{3}".format(
        MqttConfigurationParameters.MQTT_BASIC_TOPIC,
        MqttConfigurationParameters.DEVICE_TOPIC,
        agv_data["id"],
        MqttConfigurationParameters.DEVICE_TELEMETRY_TOPIC
    )
    senml_payload = [
        {"bn": f"{agv_data['id']}/"}, #bn: base name (subject external ID)
        {"n": "battery_level", "v": telemetry_data.BatteryLevel, "u": "%"}, #n: name (external ID), u: unit, v: value
        {"n": "on_off", "vs": telemetry_data.ON_OFF},  # vs: value string
        {"n": "mission_coordinates_x", "v": telemetry_data.MissionCoordinates.x},
        {"n": "mission_coordinates_y", "v": telemetry_data.MissionCoordinates.y},
        {"n": "x", "v": telemetry_data.Position.x},
        {"n": "y", "v": telemetry_data.Position.y},
        {"n": "mission_status", "vs": telemetry_data.MissionStatus},
        {"n": "timestamp", "v": telemetry_data.timestamp}
    ]
    device_payload_string = json.dumps(senml_payload)
    mqtt_client.publish(target_topic, device_payload_string, 1, True) # mqtt_client.publish(target_topic, device_payload_string, QoS (1), il broker conserva il messaggio (True))
    print(f"Telemetry data Published: Topic: {target_topic} Payload: {device_payload_string}")

def publish_device_info(agv_data):
    # device info topic: iot/user/<user_id>/device/<device_id>/info
    target_topic = "{0}/{1}/{2}/{3}".format(
        MqttConfigurationParameters.MQTT_BASIC_TOPIC,
        MqttConfigurationParameters.DEVICE_TOPIC,
        agv_data["id"],
        MqttConfigurationParameters.DEVICE_INFO_TOPIC
    )
    device_info = AGVDescriptor(agv_data["id"], agv_data["manufacturer"], agv_data["model"], agv_data["software_ver"])
    senml_device_info = [
        {"bn": f"{agv_data['id']}/"},
        {"n": "device/manufacturer", "vs": device_info.manufacturer},
        {"n": "device/model", "vs": device_info.model},
        {"n": "device/software_ver", "vs": device_info.software_ver}
    ]
    device_payload_string = json.dumps(senml_device_info)
    mqtt_client.publish(target_topic, device_payload_string, 0, False) # False: non conserverà il messaggio
    print(f"Device Info Published: Topic: {target_topic} Payload: {device_payload_string}")

message_limit = 3000

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set(MqttConfigurationParameters.MQTT_USERNAME, MqttConfigurationParameters.MQTT_PASSWORD)
mqtt_client.connect(MqttConfigurationParameters.BROKER_ADDRESS, MqttConfigurationParameters.BROKER_PORT)
mqtt_client.loop_start()

with open('../InfoData.json','r') as file:
    AGVdata = json.load(file)


for agv in AGVdata:
    publish_device_info(agv)

for agv_info in AGVdata:
    agv_info['telemetry_data'] = AGVTelemetryData()

for message_id in range(message_limit):
    for agv_info in AGVdata:
        agv_telemetry = agv_info['telemetry_data']
        agv_telemetry.update_measurements()
        publish_telemetry_data(agv_info, agv_telemetry)
        time.sleep(2)

mqtt_client.loop_stop()