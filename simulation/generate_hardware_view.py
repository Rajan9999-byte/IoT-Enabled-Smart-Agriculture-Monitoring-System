from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.patches import (
    Circle,
    Rectangle,
    FancyBboxPatch,
    FancyArrowPatch
)


ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "farm_data.csv"
OUTPUT_FILE = ROOT / "images" / "hardware_view.png"


def wire(x1, y1, x2, y2, width=2):

    ax.plot(
        [x1, x2],
        [y1, y2],
        color="black",
        linewidth=width
    )


def gpio_label(text, x, y):

    ax.text(
        x,
        y,
        text,
        fontsize=8,
        fontweight="bold"
    )


df = pd.read_csv(DATA_FILE)

latest = df.iloc[-1]

temp = latest["temperature"]
humidity = latest["humidity"]
soil = latest["soil_moisture"]
water = latest["water_level"]
pump = latest["pump_status"]


fig, ax = plt.subplots(
    figsize=(18, 10)
)

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

ax.axis("off")

fig.patch.set_facecolor("#f4f7fb")


# ==========================================================
# TITLE
# ==========================================================

ax.text(
    50,
    96,
    "IoT Enabled Smart Agriculture Monitoring System",
    ha="center",
    fontsize=24,
    fontweight="bold"
)

ax.text(
    50,
    91,
    "Virtual IoT Hardware Simulation",
    ha="center",
    fontsize=14
)


# ==========================================================
# ESP32
# ==========================================================

esp32 = FancyBboxPatch(
    (38, 35),
    24,
    34,
    boxstyle="round,pad=0.5",
    facecolor="#2f3640",
    edgecolor="black",
    linewidth=2
)

ax.add_patch(esp32)

chip = Rectangle(
    (44, 47),
    12,
    10,
    facecolor="#111111",
    edgecolor="white"
)

ax.add_patch(chip)

ax.text(
    50,
    58,
    "ESP32",
    fontsize=20,
    color="white",
    fontweight="bold",
    ha="center"
)

ax.text(
    50,
    54,
    "DEVKIT V1",
    fontsize=10,
    color="white",
    ha="center"
)

for y in range(38, 68, 2):

    ax.add_patch(
        Rectangle(
            (37, y),
            1,
            1,
            facecolor="#3498db"
        )
    )

    ax.add_patch(
        Rectangle(
            (62, y),
            1,
            1,
            facecolor="#3498db"
        )
    )

gpio_label("GPIO4", 34, 62)
gpio_label("GPIO34", 32, 55)
gpio_label("GPIO35", 32, 48)
gpio_label("GPIO26", 63, 40)


# ==========================================================
# DHT22
# ==========================================================

dht = Rectangle(
    (10, 70),
    12,
    12,
    facecolor="#4aa3df",
    edgecolor="black"
)

ax.add_patch(dht)

for i in range(5):
    for j in range(5):

        ax.add_patch(
            Circle(
                (12 + i * 1.8, 72 + j * 1.8),
                0.2,
                color="white"
            )
        )

ax.text(
    16,
    84,
    "DHT22",
    fontsize=12,
    fontweight="bold",
    ha="center"
)


# ==========================================================
# SOIL SENSOR
# ==========================================================

soil_module = Rectangle(
    (24, 74),
    10,
    4,
    facecolor="#27ae60",
    edgecolor="black"
)

ax.add_patch(soil_module)

ax.add_patch(
    Rectangle(
        (27, 62),
        1,
        12,
        facecolor="silver",
        edgecolor="black"
    )
)

ax.add_patch(
    Rectangle(
        (30, 62),
        1,
        12,
        facecolor="silver",
        edgecolor="black"
    )
)

ax.text(
    29,
    81,
    "SOIL MOISTURE",
    fontsize=11,
    fontweight="bold",
    ha="center"
)


# ==========================================================
# LDR
# ==========================================================

ldr = Circle(
    (68, 76),
    4,
    facecolor="#f4c542",
    edgecolor="black"
)

ax.add_patch(ldr)

ax.text(
    68,
    84,
    "LDR",
    fontsize=12,
    fontweight="bold",
    ha="center"
)


# ==========================================================
# WATER TANK
# ==========================================================

tank = Rectangle(
    (80, 68),
    10,
    16,
    facecolor="white",
    edgecolor="black",
    linewidth=2
)

ax.add_patch(tank)

fill_height = 16 * (water / 100)

ax.add_patch(
    Rectangle(
        (80, 68),
        10,
        fill_height,
        facecolor="#3498db"
    )
)

ax.text(
    85,
    86,
    "WATER TANK",
    fontsize=12,
    fontweight="bold",
    ha="center"
)


# ==========================================================
# WATER LEVEL SENSOR
# ==========================================================

water_sensor = Rectangle(
    (74, 72),
    3,
    8,
    facecolor="#95a5a6",
    edgecolor="black"
)

ax.add_patch(water_sensor)

ax.text(
    75.5,
    82,
    "LEVEL",
    fontsize=8,
    ha="center"
)


# ==========================================================
# RELAY
# ==========================================================

relay = Rectangle(
    (12, 15),
    16,
    10,
    facecolor="#2980b9",
    edgecolor="black"
)

ax.add_patch(relay)

ax.text(
    20,
    20,
    "RELAY",
    fontsize=12,
    color="white",
    fontweight="bold",
    ha="center"
)

ax.text(
    20,
    16,
    "COM NO NC",
    fontsize=7,
    ha="center"
)


# ==========================================================
# PUMP
# ==========================================================

pump_body = Circle(
    (82, 20),
    6,
    facecolor="#16a085",
    edgecolor="black"
)

ax.add_patch(pump_body)

pump_center = Circle(
    (82, 20),
    2,
    facecolor="white"
)

ax.add_patch(pump_center)

ax.text(
    82,
    29,
    "WATER PUMP",
    fontsize=11,
    fontweight="bold",
    ha="center"
)

# ==========================================================
# HTTP GATEWAY
# ==========================================================

gateway = Rectangle(
    (68, 46),
    20,
    10,
    facecolor="#8e44ad",
    edgecolor="black"
)

ax.add_patch(gateway)

ax.text(
    78,
    51,
    "HTTP",
    color="white",
    fontsize=12,
    fontweight="bold",
    ha="center"
)

ax.text(
    78,
    47,
    "IoT Gateway",
    color="white",
    fontsize=10,
    ha="center"
)


# ==========================================================
# DASHBOARD
# ==========================================================

dashboard = Rectangle(
    (68, 32),
    20,
    8,
    facecolor="#34495e",
    edgecolor="black"
)

ax.add_patch(dashboard)

ax.text(
    78,
    36,
    "Dashboard",
    color="white",
    fontsize=11,
    ha="center"
)


# ==========================================================
# DECISION ENGINE
# ==========================================================

decision = Rectangle(
    (68, 60),
    20,
    8,
    facecolor="#e67e22",
    edgecolor="black"
)

ax.add_patch(decision)

ax.text(
    78,
    64,
    "Decision Engine",
    fontsize=10,
    color="white",
    fontweight="bold",
    ha="center"
)


# ==========================================================
# FIELD / CROPLAND
# ==========================================================

field = Rectangle(
    (22, 4),
    26,
    8,
    facecolor="#8b5a2b",
    edgecolor="black"
)

ax.add_patch(field)

ax.text(
    35,
    8,
    "TOMATO FIELD",
    fontsize=11,
    color="white",
    fontweight="bold",
    ha="center"
)


# ==========================================================
# IRRIGATION PIPE
# ==========================================================

ax.plot(
    [82, 82],
    [14, 10],
    linewidth=5,
    color="#3498db"
)

ax.plot(
    [82, 35],
    [10, 10],
    linewidth=5,
    color="#3498db"
)

ax.text(
    60,
    12,
    "Irrigation Pipeline",
    fontsize=9,
    color="#21618c"
)


# ==========================================================
# WATER FLOW DROPS
# ==========================================================

for x in [72, 62, 52, 42]:

    drop = Circle(
        (x, 10),
        0.6,
        facecolor="#3498db",
        edgecolor="#3498db"
    )

    ax.add_patch(drop)


# ==========================================================
# FEEDBACK LOOP
# ==========================================================

feedback = FancyArrowPatch(
    (35, 12),
    (29, 62),
    arrowstyle="->",
    mutation_scale=20,
    linewidth=2,
    linestyle="--",
    color="green"
)

ax.add_patch(feedback)

ax.text(
    18,
    38,
    "Soil Moisture\nFeedback",
    fontsize=9,
    color="green"
)

# ==========================================================
# SENSOR WIRING
# ==========================================================

wire(22, 76, 32, 76)
wire(32, 76, 32, 62)
wire(32, 62, 38, 62)

wire(29, 62, 34, 62)
wire(34, 62, 34, 55)
wire(34, 55, 38, 55)

wire(68, 72, 68, 48)
wire(68, 48, 62, 48)

wire(74, 76, 74, 44)
wire(74, 44, 62, 44)


# ==========================================================
# ESP32 TO DECISION ENGINE
# ==========================================================

wire(
    62,
    64,
    68,
    64
)


# ==========================================================
# DECISION ENGINE TO RELAY
# ==========================================================

wire(
    68,
    62,
    30,
    62
)

wire(
    30,
    62,
    30,
    25
)

wire(
    30,
    25,
    28,
    25
)


# ==========================================================
# RELAY TO PUMP
# ==========================================================

wire(
    28,
    20,
    76,
    20
)


# ==========================================================
# ESP32 TO GATEWAY
# ==========================================================

wire(
    62,
    50,
    68,
    50
)


# ==========================================================
# GATEWAY TO DASHBOARD
# ==========================================================

wire(
    78,
    46,
    78,
    40
)


# ==========================================================
# WATER TANK TO PUMP
# ==========================================================

wire(
    85,
    68,
    85,
    26
)

wire(
    85,
    26,
    82,
    26
)

# ==========================================================
# LIVE SENSOR PANEL
# ==========================================================

health = "HEALTHY"

if soil < 30:
    health = "WARNING"

status_color = (
    "green"
    if pump == "OFF"
    else "orange"
)

panel_text = (
    f"Temperature : {temp:.1f} °C\n"
    f"Humidity : {humidity:.1f} %\n"
    f"Soil Moisture : {soil:.1f} %\n"
    f"Water Tank : {water:.1f} %\n"
    f"Pump : {pump}\n"
    f"Farm Health : {health}"
)

ax.text(
    4,
    46,
    panel_text,
    fontsize=13,
    bbox=dict(
        facecolor="white",
        edgecolor=status_color,
        boxstyle="round,pad=0.6"
    )
)


# ==========================================================
# FOOTER
# ==========================================================

ax.text(
    50,
    2,
    "Sensors → ESP32 → Decision Engine → Relay → Pump → Irrigation → Soil Feedback",
    ha="center",
    fontsize=11,
    style="italic"
)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

print()
print("Generated:")
print(OUTPUT_FILE)