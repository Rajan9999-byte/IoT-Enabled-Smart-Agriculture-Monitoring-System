#dashboard

from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="IoT Smart Agriculture Dashboard",
    page_icon="🌱",
    layout="wide"
)

DATA_FILE = Path(
    "data/farm_data.csv"
)

st.title(
    "🌱 IoT Enabled Smart Agriculture Monitoring System"
)

st.caption(
    "Virtual ESP32 → HTTP → IoT Gateway → Smart Irrigation Dashboard"
)

if not DATA_FILE.exists():

    st.error(
        "No IoT data found."
    )

    st.stop()

df = pd.read_csv(
    DATA_FILE
)

if df.empty:

    st.error(
        "No records available."
    )

    st.stop()

latest = df.iloc[-1]

st.markdown("---")

st.subheader(
    "IoT Architecture"
)

arch1, arch2, arch3, arch4, arch5 = st.columns(5)

with arch1:
    st.success("📡 Sensors")

with arch2:
    st.success("🖥 Virtual ESP32")

with arch3:
    st.success("🌐 HTTP")

with arch4:
    st.success("☁ IoT Gateway")

with arch5:
    st.success("🚰 Irrigation")

st.markdown("---")

top1, top2, top3, top4 = st.columns(4)

with top1:

    st.metric(
        "Farm",
        latest["farm_name"]
    )

with top2:

    st.metric(
        "Field",
        latest["field_id"]
    )

with top3:

    st.metric(
        "Crop",
        latest["crop_type"]
    )

with top4:

    st.metric(
        "Health",
        latest["farm_health"]
    )

st.markdown("---")

st.subheader(
    "Current Farm Conditions"
)

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Temperature",
        f"{latest['temperature']:.1f} °C"
    )

    st.metric(
        "Humidity",
        f"{latest['humidity']:.1f} %"
    )

with c2:

    st.metric(
        "Soil Moisture",
        f"{latest['soil_moisture']:.1f} %"
    )

    st.metric(
        "Light Intensity",
        f"{latest['light_intensity']:.0f} Lux"
    )

with c3:

    st.metric(
        "Water Tank",
        f"{latest['water_level']:.1f} %"
    )

    st.metric(
        "Pump Status",
        latest["pump_status"]
    )

st.markdown("---")

health_score = 100

if latest["temperature"] > 35:
    health_score -= 20

if latest["soil_moisture"] < 35:
    health_score -= 40

if latest["water_level"] < 25:
    health_score -= 40

health_score = max(
    0,
    health_score
)

left, right = st.columns(
    [1, 2]
)

with left:

    st.subheader(
        "Farm Health"
    )

    st.progress(
        health_score / 100
    )

    st.metric(
        "Health Score",
        f"{health_score}/100"
    )

    irrigation_events = (
        df["pump_status"] == "ON"
    ).sum()

    st.metric(
        "Irrigation Events",
        irrigation_events
    )

with right:

    st.subheader(
        "Decision Engine"
    )

    recommendation = latest[
        "recommendation"
    ]

    if latest[
        "farm_health"
    ] == "HEALTHY":

        st.success(
            recommendation
        )

    elif latest[
        "farm_health"
    ] == "WARNING":

        st.warning(
            recommendation
        )

    else:

        st.error(
            recommendation
        )

st.markdown("---")

trend1, trend2 = st.columns(2)

with trend1:

    st.subheader(
        "Soil Moisture Trend"
    )

    st.line_chart(
        df.set_index(
            "cycle"
        )[
            "soil_moisture"
        ],
        height=250
    )

with trend2:

    st.subheader(
        "Water Tank Trend"
    )

    st.line_chart(
        df.set_index(
            "cycle"
        )[
            "water_level"
        ],
        height=250
    )

st.markdown("---")

st.caption(
    "Virtual IoT Agriculture Platform"
)