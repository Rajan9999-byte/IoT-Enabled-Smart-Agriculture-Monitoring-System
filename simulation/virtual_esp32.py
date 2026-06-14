#virtual_esp32

import random
import time

import requests

GATEWAY_URL = "http://127.0.0.1:5000/sensor-data"

TOTAL_CYCLES = 100

soil_moisture = 80.0
water_level = 100.0

pump_active = False
pump_cycles_remaining = 0

tank_refill_active = False
tank_refill_cycles_remaining = 0

print()
print("=" * 60)
print("VIRTUAL ESP32 DEVICE STARTED")
print("=" * 60)
print()

for cycle in range(1, TOTAL_CYCLES + 1):

    if 1 <= cycle <= 20:

        temperature = random.uniform(
            24,
            30
        )

        humidity = random.uniform(
            65,
            85
        )

    elif 21 <= cycle <= 40:

        temperature = random.uniform(
            35,
            42
        )

        humidity = random.uniform(
            40,
            60
        )

    elif 41 <= cycle <= 60:

        temperature = random.uniform(
            28,
            34
        )

        humidity = random.uniform(
            50,
            75
        )

    elif 61 <= cycle <= 80:

        temperature = random.uniform(
            37,
            44
        )

        humidity = random.uniform(
            35,
            55
        )

    else:

        temperature = random.uniform(
            24,
            30
        )

        humidity = random.uniform(
            60,
            90
        )

    light_intensity = random.uniform(
        250,
        1000
    )

    evaporation = random.uniform(
        0.5,
        1.2
    )

    evaporation += (
        max(
            0,
            temperature - 30
        ) * 0.08
    )

    soil_moisture -= evaporation

    if soil_moisture < 30 and not pump_active:

        pump_active = True
        pump_cycles_remaining = 5

    if pump_active:

        soil_moisture += random.uniform(
            2,
            4
        )

        water_level -= random.uniform(
            1,
            2
        )

        pump_cycles_remaining -= 1

        if pump_cycles_remaining <= 0:

            pump_active = False

    if water_level < 25 and not tank_refill_active:

        tank_refill_active = True
        tank_refill_cycles_remaining = 8

        print()
        print(
            "TANK REFILL STARTED"
        )
        print()

    if tank_refill_active:

        water_level += random.uniform(
            4,
            8
        )

        tank_refill_cycles_remaining -= 1

        if tank_refill_cycles_remaining <= 0:

            tank_refill_active = False

            print()
            print(
                "TANK REFILL COMPLETED"
            )
            print()

    soil_moisture = max(
        0,
        min(
            100,
            soil_moisture
        )
    )

    water_level = max(
        0,
        min(
            100,
            water_level
        )
    )

    pump_status = (
        "ON"
        if pump_active
        else "OFF"
    )

    payload = {

        "cycle":
        cycle,

        "temperature":
        round(
            temperature,
            1
        ),

        "humidity":
        round(
            humidity,
            1
        ),

        "soil_moisture":
        round(
            soil_moisture,
            1
        ),

        "light_intensity":
        round(
            light_intensity,
            1
        ),

        "water_level":
        round(
            water_level,
            1
        ),

        "pump_status":
        pump_status
    }

    try:

        response = requests.post(
            GATEWAY_URL,
            json=payload,
            timeout=10
        )

        print(
            f"[{cycle:03d}/{TOTAL_CYCLES}] "
            f"T={temperature:.1f}°C "
            f"H={humidity:.1f}% "
            f"Soil={soil_moisture:.1f}% "
            f"Water={water_level:.1f}% "
            f"Pump={pump_status} "
            f"HTTP={response.status_code}"
        )

    except Exception as error:

        print(
            f"Gateway Error: {error}"
        )

    time.sleep(1)

print()
print("=" * 60)
print("SIMULATION COMPLETE")
print("=" * 60)
print()