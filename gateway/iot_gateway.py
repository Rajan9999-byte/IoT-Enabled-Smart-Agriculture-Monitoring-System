#iot_gateway

from pathlib import Path
from datetime import datetime
import json

import pandas as pd
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = BASE_DIR / "config" / "farm_config.json"

DATA_FILE = BASE_DIR / "data" / "farm_data.csv"

ALERT_FILE = BASE_DIR / "outputs" / "alerts.log"

REPORT_FILE = BASE_DIR / "outputs" / "daily_report.txt"


def load_config():

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


CONFIG = load_config()


def determine_status(
    temperature,
    soil_moisture,
    water_level
):

    if (
        temperature > 38
        or soil_moisture < 20
        or water_level < 10
    ):

        return (
            "CRITICAL",
            "Immediate irrigation attention required."
        )

    if (
        temperature > 34
        or soil_moisture < 35
        or water_level < 25
    ):

        return (
            "WARNING",
            "Monitor field conditions closely."
        )

    return (
        "HEALTHY",
        "Field operating under normal conditions."
    )


def create_storage():

    DATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    ALERT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not DATA_FILE.exists():

        columns = [
            "timestamp",
            "cycle",
            "farm_name",
            "field_id",
            "crop_type",
            "temperature",
            "humidity",
            "soil_moisture",
            "light_intensity",
            "water_level",
            "pump_status",
            "farm_health",
            "recommendation"
        ]

        pd.DataFrame(
            columns=columns
        ).to_csv(
            DATA_FILE,
            index=False
        )


create_storage()


@app.route(
    "/",
    methods=["GET"]
)
def home():

    return jsonify(
        {
            "service":
            "IoT Smart Agriculture Gateway",
            "status":
            "running"
        }
    )


@app.route(
    "/sensor-data",
    methods=["POST"]
)
def receive_sensor_data():

    payload = request.json

    temperature = float(
        payload["temperature"]
    )

    humidity = float(
        payload["humidity"]
    )

    soil_moisture = float(
        payload["soil_moisture"]
    )

    light_intensity = float(
        payload["light_intensity"]
    )

    water_level = float(
        payload["water_level"]
    )

    pump_status = payload[
        "pump_status"
    ]

    cycle = int(
        payload["cycle"]
    )

    farm_health, recommendation = (
        determine_status(
            temperature,
            soil_moisture,
            water_level
        )
    )

    row = {

        "timestamp":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "cycle":
        cycle,

        "farm_name":
        CONFIG["farm_name"],

        "field_id":
        CONFIG["field_id"],

        "crop_type":
        CONFIG["crop_type"],

        "temperature":
        temperature,

        "humidity":
        humidity,

        "soil_moisture":
        soil_moisture,

        "light_intensity":
        light_intensity,

        "water_level":
        water_level,

        "pump_status":
        pump_status,

        "farm_health":
        farm_health,

        "recommendation":
        recommendation
    }

    pd.DataFrame(
        [row]
    ).to_csv(
        DATA_FILE,
        mode="a",
        header=False,
        index=False
    )

    if farm_health != "HEALTHY":

        with open(
            ALERT_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                f"{row['timestamp']} | "
                f"{farm_health} | "
                f"{recommendation}\n"
            )

    build_report()

    return jsonify(
        {
            "message":
            "Sensor data received",
            "status":
            farm_health
        }
    )


def build_report():

    try:

        df = pd.read_csv(
            DATA_FILE
        )

        if df.empty:
            return

        latest = df.iloc[-1]

        report = f"""
IoT ENABLED SMART AGRICULTURE MONITORING SYSTEM

Farm Name: {latest['farm_name']}
Field ID: {latest['field_id']}
Crop Type: {latest['crop_type']}

Current Status
--------------
Temperature : {latest['temperature']}
Humidity : {latest['humidity']}
Soil Moisture : {latest['soil_moisture']}
Light Intensity : {latest['light_intensity']}
Water Level : {latest['water_level']}
Pump Status : {latest['pump_status']}

Farm Health : {latest['farm_health']}
Recommendation :
{latest['recommendation']}
"""

        with open(
            REPORT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                report
            )

    except Exception:

        pass


if __name__ == "__main__":

    print()

    print(
        "=" * 60
    )

    print(
        "IoT SMART AGRICULTURE GATEWAY STARTED"
    )

    print(
        "=" * 60
    )

    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )