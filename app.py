import math
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Nassau Candy Decision Intelligence",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)

FACTORIES = {
    "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036, "base_cost_multiplier": 1.15},
    "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371, "base_cost_multiplier": 1.05},
    "Sugar Shack": {"lat": 48.11914, "lon": -96.18115, "base_cost_multiplier": 1.00},
    "Secret Factory": {"lat": 41.446333, "lon": -90.565487, "base_cost_multiplier": 1.10},
    "The Other Factory": {"lat": 35.1175, "lon": -89.971107, "base_cost_multiplier": 1.08},
}

REGIONS_COORDS = {
    "Atlantic": {"lat": 40.00, "lon": -74.50},
    "Gulf": {"lat": 30.00, "lon": -90.00},
    "Interior": {"lat": 38.50, "lon": -97.00},
    "Pacific": {"lat": 37.00, "lon": -120.00},
}

PRODUCT_REGISTRY = {
    "Wonka Bar - Nutty Crunch Surprise": {"Division": "Chocolate", "Factory": "Lot's O' Nuts"},
    "Wonka Bar - Fudge Mallows": {"Division": "Chocolate", "Factory": "Lot's O' Nuts"},
    "Wonka Bar -Scrumdiddlyumptious": {"Division": "Chocolate", "Factory": "Lot's O' Nuts"},
    "Wonka Bar - Milk Chocolate": {"Division": "Chocolate", "Factory": "Wicked Choccy's"},
    "Wonka Bar - Triple Dazzle Caramel": {"Division": "Chocolate", "Factory": "Wicked Choccy's"},
    "Laffy Taffy": {"Division": "Sugar", "Factory": "Sugar Shack"},
    "SweeTARTS": {"Division": "Sugar", "Factory": "Sugar Shack"},
    "Nerds": {"Division": "Sugar", "Factory": "Sugar Shack"},
    "Fun Dip": {"Division": "Sugar", "Factory": "Sugar Shack"},
    "Fizzy Lifting Drinks": {"Division": "Other", "Factory": "Sugar Shack"},
    "Everlasting Gobstopper": {"Division": "Sugar", "Factory": "Secret Factory"},
    "Hair Toffee": {"Division": "Sugar", "Factory": "The Other Factory"},
    "Lickable Wallpaper": {"Division": "Other", "Factory": "Secret Factory"},
    "Wonka Gum": {"Division": "Other", "Factory": "Secret Factory"},
    "Kazookles": {"Division": "Other", "Factory": "The Other Factory"},
}

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

@st.cache_data
def load_historical_ledger_file():
    try:
        df = pd.read_csv("nassau_candy_orders.csv")
        df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
        df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y", errors="coerce")
        df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
        return df.dropna(subset=["Lead Time"])
    except Exception as e:
        st.warning(f"⚠️ Could not load 'nassau_candy_orders.csv': {e}")
        return pd.DataFrame()

df_orders = load_historical_ledger_file()

st.sidebar.title("🍬 Master Control Panel")
st.sidebar.markdown("---")

available_products = list(PRODUCT_REGISTRY.keys())
available_regions = list(REGIONS_COORDS.keys())
available_ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]

ui_product = st.sidebar.selectbox("🎯 Target Product Line", available_products)
ui_region = st.sidebar.selectbox("🗺️ Destination Corridor", available_regions)
ui_ship_mode = st.sidebar.selectbox("⚡ Contracted Ship Mode", available_ship_modes)

weight_profit = st.sidebar.slider("Priority Balance Allocation (Speed vs Profit)", 0.0, 1.0, 0.50, step=0.05)
weight_speed = 1.0 - weight_profit

current_legacy_factory = PRODUCT_REGISTRY[ui_product]["Factory"]
dest_lat = REGIONS_COORDS[ui_region]["lat"]
dest_lon = REGIONS_COORDS[ui_region]["lon"]

matrix_sim_records = []
absolute_optimum_factory = current_legacy_factory
highest_utility_score = float("inf")
ship_base_days = {"Standard Class": 5.5, "Second Class": 3.5, "First Class": 1.8, "Same Day": 0.5}[ui_ship_mode]

for factory_node, details in FACTORIES.items():
    distance_km = calculate_haversine_distance(details["lat"], details["lon"], dest_lat, dest_lon)
    simulated_lead_time = max(0.5, round(ship_base_days + (distance_km / 750.0), 2))
    margin_erosion_delta = round((details["base_cost_multiplier"] - 1.00) * 120.0, 2)
    utility_score = (simulated_lead_time * weight_speed * 15.0) + (margin_erosion_delta * weight_profit * 8.0)

    matrix_sim_records.append({
        "Factory": factory_node,
        "Distance (km)": round(distance_km, 1),
        "Predicted Lead Time (Days)": simulated_lead_time,
        "Margin Delta ($)": round(-margin_erosion_delta, 2),
        "Utility Score": utility_score,
        "Is Legacy": factory_node == current_legacy_factory
    })

    if utility_score < highest_utility_score:
        highest_utility_score = utility_score
        absolute_optimum_factory = factory_node

matrix_sim_records = sorted(matrix_sim_records, key=lambda x: x["Utility Score"])
legacy_metrics = next(x for x in matrix_sim_records if x["Factory"] == current_legacy_factory)
optimal_metrics = next(x for x in matrix_sim_records if x["Factory"] == absolute_optimum_factory)

lead_time_gain_pct = max(0.0, ((legacy_metrics["Predicted Lead Time (Days)"] - optimal_metrics["Predicted Lead Time (Days)"]) / legacy_metrics["Predicted Lead Time (Days)"]) * 100)

st.session_state["df_orders"] = df_orders
st.session_state["ui_product"] = ui_product
st.session_state["ui_region"] = ui_region
st.session_state["ui_ship_mode"] = ui_ship_mode
st.session_state["weight_profit"] = weight_profit
st.session_state["weight_speed"] = weight_speed
st.session_state["current_legacy_factory"] = current_legacy_factory
st.session_state["absolute_optimum_factory"] = absolute_optimum_factory
st.session_state["matrix_sim_records"] = matrix_sim_records
st.session_state["legacy_metrics"] = legacy_metrics
st.session_state["optimal_metrics"] = optimal_metrics
st.session_state["lead_time_gain_pct"] = lead_time_gain_pct

st.title("🍬 Nassau Candy Decision Intelligence Platform")
st.markdown("---")

st.markdown("""
### 🚀 Systems Workspace Welcome Directive
Use the sidebar navigation links to view system modules:
- **📊 Factory Optimization Simulator:** Review full candidate node prediction latency metrics.
- **🔄 What-If Scenario Analysis:** Compare routing paths and parameter weight changes.
- **📋 Recommendations:** View ranked facility suitability indices and efficiency summaries.
- **⚠️ Risk & Impact Panel:** Inspect automated safe horizon guardrails and margin metrics logs.
""")

st.markdown("<br>", unsafe_allow_html=True)
k_cols = st.columns(3)
with k_cols[0]:
    st.metric("Factual Records Processed", f"{len(df_orders):,}")
with k_cols[1]:
    st.metric("Active Catalog Item Filter Focus", ui_product)
with k_cols[2]:
    st.metric("Max Latency Optimization Cap", f"{lead_time_gain_pct:.1f}% Days Saved")