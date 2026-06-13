"""MQTT subscriber for QoS test messages."""

from __future__ import annotations

import paho.mqtt.client as mqtt


def log(message: str) -> None:
    """Print log message immediately."""
    print(message, flush=True)

BROKER = "localhost"
PORT = 1883
KEEPALIVE = 60
TOPIC = "smartroom/qos/test"
SUBSCRIBE_QOS = 2


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
        client.subscribe(TOPIC, qos=SUBSCRIBE_QOS)
        log(f"[SUBSCRIBED] {TOPIC} | QoS: {SUBSCRIBE_QOS}")
    else:
        log(f"[ERROR] Connection failed: {reason_code}")


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    log(f"[RECEIVED] Topic: {message.topic} | Payload: {payload} | QoS: {message.qos}")


def main() -> None:
    broker = input(f"Enter broker host [{BROKER}]: ").strip() or BROKER
    port_input = input(f"Enter broker port [{PORT}]: ").strip()
    try:
        port = int(port_input) if port_input else PORT
    except ValueError:
        log(f"Invalid port, using default {PORT}")
        port = PORT

    qos_input = input(f"Enter QoS level to subscribe (0, 1, 2) [{SUBSCRIBE_QOS}]: ").strip()
    try:
        subscribe_qos = int(qos_input) if qos_input else SUBSCRIBE_QOS
        if subscribe_qos not in (0, 1, 2):
            raise ValueError
    except ValueError:
        log(f"Invalid QoS level, using default {SUBSCRIBE_QOS}")
        subscribe_qos = SUBSCRIBE_QOS

    client = create_client()
    
    def on_connect_local(client, userdata, flags, reason_code, properties=None):
        if is_success(reason_code):
            log(f"[CONNECTED] Broker {broker}:{port}")
            client.subscribe(TOPIC, qos=subscribe_qos)
            log(f"[SUBSCRIBED] {TOPIC} | QoS: {subscribe_qos}")
        else:
            log(f"[ERROR] Connection failed: {reason_code}")

    client.on_connect = on_connect_local
    client.on_message = on_message

    log(f"[CONNECTING] Broker {broker}:{port}")
    client.connect(broker, port, KEEPALIVE)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        log("\n[STOPPED]")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
