"""MQTT publisher for smart room monitoring."""

from __future__ import annotations

import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
KEEPALIVE = 60


def generate_sensor_messages() -> list[tuple[str, str, int]]:
    return [
        ("smartroom/room1/temperature", f"{random.uniform(20.0, 30.0):.1f}", 0),
        ("smartroom/room1/humidity", f"{random.randint(40, 80)}", 0),
        ("smartroom/room1/light", random.choice(["ON", "OFF"]), 0),
        ("smartroom/room2/temperature", f"{random.uniform(20.0, 30.0):.1f}", 0),
        ("smartroom/room2/humidity", f"{random.randint(40, 80)}", 0),
        ("smartroom/room2/light", random.choice(["ON", "OFF"]), 0),
    ]

QOS_MESSAGES = [
    ("smartroom/qos/test", "Test QoS 0", 0),
    ("smartroom/qos/test", "Test QoS 1", 1),
    ("smartroom/qos/test", "Test QoS 2", 2),
]


def create_client() -> mqtt.Client:
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except AttributeError:
        return mqtt.Client()


def main() -> None:
    broker = input(f"Enter broker host [{BROKER}]: ").strip() or BROKER
    port_input = input(f"Enter broker port [{PORT}]: ").strip()
    try:
        port = int(port_input) if port_input else PORT
    except ValueError:
        print(f"Invalid port, using default {PORT}")
        port = PORT

    client = create_client()

    try:
        print(f"[CONNECTING] Broker {broker}:{port}")
        client.connect(broker, port, KEEPALIVE)
        client.loop_start()
        time.sleep(0.3)
        print(f"[CONNECTED] Broker {broker}:{port}")

        while True:
            print("\n--- MQTT Publisher Menu ---")
            print("1. Start automated loop (publishes randomized sensor readings every 5 seconds)")
            print("2. Publish a custom message")
            print("3. Exit")
            choice = input("Choose option: ").strip()

            if choice == "1":
                print("[INFO] Starting automated loop. Press Ctrl+C to return to menu.")
                try:
                    while True:
                        for topic, payload, qos in generate_sensor_messages():
                            result = client.publish(topic, payload, qos=qos)
                            result.wait_for_publish()
                            print(f"[PUBLISHED] Topic: {topic} | Payload: {payload} | QoS: {qos}")
                        time.sleep(5)
                except KeyboardInterrupt:
                    print("\n[LOOP STOPPED]")
            elif choice == "2":
                topic = input("Enter topic: ").strip()
                if not topic:
                    print("[ERROR] Topic cannot be empty.")
                    continue
                payload = input("Enter payload: ")
                qos_input = input("Enter QoS (0, 1, 2) [0]: ").strip()
                try:
                    qos = int(qos_input) if qos_input else 0
                    if qos not in (0, 1, 2):
                        raise ValueError
                except ValueError:
                    print("[WARNING] Invalid QoS. Defaulting to QoS 0.")
                    qos = 0
                
                result = client.publish(topic, payload, qos=qos)
                result.wait_for_publish()
                print(f"[PUBLISHED] Topic: {topic} | Payload: {payload} | QoS: {qos}")
            elif choice == "3":
                break
            else:
                print("[ERROR] Invalid choice. Please select 1, 2, or 3.")
    except KeyboardInterrupt:
        print("\n[STOPPED]")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[DISCONNECTED]")



if __name__ == "__main__":
    main()
