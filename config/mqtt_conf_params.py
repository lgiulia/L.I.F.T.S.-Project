
class MqttConfigurationParameters(object):
    BROKER_ADDRESS =  "155.185.4.4"
    BROKER_PORT = 7883
    MQTT_USERNAME = "308955@studenti.unimore.it"
    MQTT_PASSWORD = "lhneynnevujikxrc"
    MQTT_BASIC_TOPIC = "/iot/user/{0}".format(MQTT_USERNAME)
    DEVICE_TOPIC = "device"
    DEVICE_TELEMETRY_TOPIC = "telemetry"
    DEVICE_INFO_TOPIC = "info"

#dobbiamo capire cosa metterci dentro strada facendo -> Risolto?