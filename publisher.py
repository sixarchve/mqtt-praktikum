"""MQTT publisher for smart room monitoring."""

from __future__ import annotations

import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
KEEPALIVE = 60

SENSOR_MESSAGES = [
    ("smartroom/room1/temperature", "27.5", 0),
    ("smartroom/room1/humidity", "70", 0),
    ("smartroom/room1/light", "ON", 0),
    ("smartroom/room2/temperature", "29.1", 0),
    ("smartroom/room2/humidity", "65", 0),
    ("smartroom/room2/light", "OFF", 0),
]

QOS_MESSAGES = [
    ("smartroom/qos/test", "Test QoS 0", 0),
    ("smartroom/qos/test", "Test QoS 1", 1),
    ("smartroom/qos/test", "Test QoS 2", 2),
]


def create_client() -> mqtt.Client:
    """Create MQTT client compatible with paho-mqtt 1.x and 2.x."""
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


def main() -> None:
    client = create_client()

    print(f"[CONNECTING] Broker {BROKER}:{PORT}")
    client.connect(BROKER, PORT, KEEPALIVE)
    client.loop_start()
    time.sleep(0.3)
    print(f"[CONNECTED] Broker {BROKER}:{PORT}")

    for topic, payload, qos in SENSOR_MESSAGES:
        result = client.publish(topic, payload, qos=qos)
        result.wait_for_publish()
        print(f"[PUBLISHED] Topic: {topic} | Payload: {payload} | QoS: {qos}")

    for topic, payload, qos in QOS_MESSAGES:
        result = client.publish(topic, payload, qos=qos)
        result.wait_for_publish()
        print(f"[PUBLISHED] Topic: {topic} | Payload: {payload} | QoS: {qos}")

    time.sleep(0.3)
    client.loop_stop()
    client.disconnect()
    print("[DISCONNECTED]")


if __name__ == "__main__":
    main()
