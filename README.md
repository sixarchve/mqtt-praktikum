# MQTT Smart Room Monitoring

A simple MQTT lab project. One publisher sends dummy sensor data, four subscribers each demonstrate a different MQTT feature: specific topics, QoS levels, and wildcards.

## File Structure

```
mqtt-praktikum/
├── publisher.py
├── subscriber_basic.py
├── subscriber_qos.py
├── subscriber_plus.py
├── subscriber_hash.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3
- Mosquitto broker
- `paho-mqtt`

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If Mosquitto isn't installed yet:

```bash
sudo apt update && sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
```

Broker runs on `localhost:1883`.

## How It Works

```
                        +----------------------+
                        |  Mosquitto Broker    |
                        |  localhost:1883      |
                        +----------+-----------+
                                   ^
                                   |
        +--------------------------+---------------------------+
        |                                                      |
+-------+--------+   smartroom/room1/temperature      +-------+----------------+
|   Publisher    |----------------------------------->| subscriber_basic.py    |
|   publisher.py |                                    | specific topic         |
+-------+--------+                                    +------------------------+
        |
        | smartroom/qos/test (QoS 0, 1, 2)
        +----------------------------------------------> subscriber_qos.py
        |
        | smartroom/+/temperature
        +----------------------------------------------> subscriber_plus.py
        |
        | smartroom/#
        +----------------------------------------------> subscriber_hash.py
```

## Topics

Format: `smartroom/{room}/{sensor}`

Sensor data published:

| Topic | Value |
|---|---|
| `smartroom/room1/temperature` | 27.5 |
| `smartroom/room1/humidity` | 70 |
| `smartroom/room1/light` | ON |
| `smartroom/room2/temperature` | 29.1 |
| `smartroom/room2/humidity` | 65 |
| `smartroom/room2/light` | OFF |

QoS test topic: `smartroom/qos/test` — published 3 times at QoS 0, 1, and 2.

## Subscribers

| File | Subscribes to | Notes |
|---|---|---|
| `subscriber_basic.py` | `smartroom/room1/temperature` | Single specific topic |
| `subscriber_qos.py` | `smartroom/qos/test` | Tests QoS differences |
| `subscriber_plus.py` | `smartroom/+/temperature` | Single-level wildcard |
| `subscriber_hash.py` | `smartroom/#` | All topics under `smartroom` |

## Running

Start a subscriber in one terminal, then run the publisher in another.

```bash
# Terminal 1 — pick one
python3 subscriber_basic.py
python3 subscriber_qos.py
python3 subscriber_plus.py
python3 subscriber_hash.py

# Terminal 2
python3 publisher.py
```

### Expected Output

**subscriber_basic.py**
```
[CONNECTED] Broker localhost:1883
[SUBSCRIBED] smartroom/room1/temperature
[RECEIVED] Topic: smartroom/room1/temperature | Payload: 27.5 | QoS: 0
```

**subscriber_qos.py**
```
[CONNECTED] Broker localhost:1883
[SUBSCRIBED] smartroom/qos/test | QoS: 2
[RECEIVED] Topic: smartroom/qos/test | Payload: Test QoS 0 | QoS: 0
[RECEIVED] Topic: smartroom/qos/test | Payload: Test QoS 1 | QoS: 1
[RECEIVED] Topic: smartroom/qos/test | Payload: Test QoS 2 | QoS: 2
```

**subscriber_plus.py**
```
[CONNECTED] Broker localhost:1883
[SUBSCRIBED] smartroom/+/temperature
[RECEIVED] Topic: smartroom/room1/temperature | Payload: 27.5 | QoS: 0
[RECEIVED] Topic: smartroom/room2/temperature | Payload: 29.1 | QoS: 0
```

**subscriber_hash.py**
```
[CONNECTED] Broker localhost:1883
[SUBSCRIBED] smartroom/#
[RECEIVED] Topic: smartroom/room1/temperature | Payload: 27.5 | QoS: 0
[RECEIVED] Topic: smartroom/room1/humidity | Payload: 70 | QoS: 0
[RECEIVED] Topic: smartroom/room1/light | Payload: ON | QoS: 0
[RECEIVED] Topic: smartroom/room2/temperature | Payload: 29.1 | QoS: 0
[RECEIVED] Topic: smartroom/room2/humidity | Payload: 65 | QoS: 0
[RECEIVED] Topic: smartroom/room2/light | Payload: OFF | QoS: 0
[RECEIVED] Topic: smartroom/qos/test | Payload: Test QoS 0 | QoS: 0
[RECEIVED] Topic: smartroom/qos/test | Payload: Test QoS 1 | QoS: 1
[RECEIVED] Topic: smartroom/qos/test | Payload: Test QoS 2 | QoS: 2
```

## QoS Levels

| Level | Behavior |
|---|---|
| QoS 0 | At most once - fire and forget, no acknowledgment |
| QoS 1 | At least once - acknowledged, but duplicates are possible |
| QoS 2 | Exactly once - 4-step handshake, guaranteed single delivery |

---

Press `Ctrl+C` to stop any subscriber.
