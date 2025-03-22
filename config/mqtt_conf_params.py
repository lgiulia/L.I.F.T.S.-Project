
class MqttConfigurationParameters(object):
    BROKER_ADDRESS =  "153.183.5.5"
    BROKER_PORT = 7883
    MQTT_USERNAME = "305609@studenti.unimore.it"
    MQTT_PASSWORD = "osklduvrzblhnjdd"
    MQTT_BASIC_TOPIC = "/iot/user/{0}".format(MQTT_USERNAME)
    DEVICE_TOPIC = "device"
    DEVICE_TELEMETRY_TOPIC = "telemetry"
    DEVICE_INFO_TOPIC = "info"

#dobbiamo capire cosa metterci dentro strada facendo -> Risolto?