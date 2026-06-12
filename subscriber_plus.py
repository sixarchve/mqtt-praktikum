"""MQTT subscriber using + wildcard for all room temperatures."""

from __future__ import annotations

import paho.mqtt.client as mqtt


def log(message: str) -> None:
    """Print log message immediately."""
    print(message, flush=True)

BROKER = "localhost"
PORT = 1883
KEEPALIVE = 60
TOPIC = "smartroom/+/temperature"


def create_client() -> mqtt.Client:
    """Create MQTT client compatible with paho-mqtt 1.x and 2.x."""
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


def is_success(reason_code) -> bool:
    """Return True when MQTT connection code means success."""
    return getattr(reason_code, "value", reason_code) == 0


def on_connect(client, userdata, flags, reason_code, properties=None):
    if is_success(reason_code):
        log(f"[CONNECTED] Broker {BROKER}:{PORT}")
        client.subscribe(TOPIC)
        log(f"[SUBSCRIBED] {TOPIC}")
    else:
        log(f"[ERROR] Connection failed: {reason_code}")


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    log(f"[RECEIVED] Topic: {message.topic} | Payload: {payload} | QoS: {message.qos}")


def main() -> None:
    client = create_client()
    client.on_connect = on_connect
    client.on_message = on_message

    log(f"[CONNECTING] Broker {BROKER}:{PORT}")
    client.connect(BROKER, PORT, KEEPALIVE)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        log("\n[STOPPED]")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
