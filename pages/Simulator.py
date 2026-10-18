import pandas as pd
import streamlit as st

st.title("📊 Factory Optimization Simulator")
st.markdown("---")

if "matrix_sim_records" not in st.session_state or "df_orders" not in st.session_state:
    st.warning("⚠️ No active simulation context found. Please run the setup parameters in the main panel first.")
    st.stop()

matrix_sim_records = st.session_state.get("matrix_sim_records", [])
ui_product = st.session_state.get("ui_product", "N/A")
ui_region = st.session_state.get("ui_region", "N/A")
df_orders = st.session_state.get("df_orders")

st.subheader("Fulfillment Network Latency Simulation Chart")
if matrix_sim_records:
    df_chart = pd.DataFrame(matrix_sim_records)
    st.bar_chart(
        df_chart,
        x="Factory",
        y="Predicted Lead Time (Days)",
        x_label="Candidate Production Facility",
        y_label="Predicted Lead Time (Days)",
    )

st.subheader("📋 Factual Shipping Records Lookup")
if df_orders is not None and not df_orders.empty:
    filtered_historical = df_orders[
        (df_orders["Product Name"] == ui_product) & (df_orders["Region"] == ui_region)
    ]
    if not filtered_historical.empty:
        display_cols = ["Order ID", "Order Date", "Ship Date", "Sales", "Units", "Gross Profit", "Lead Time"]
        valid_cols = [col for col in display_cols if col in filtered_historical.columns]
        st.dataframe(filtered_historical[valid_cols], use_container_width=True)
    else:
        st.caption("No historical records match this product-to-region corridor.")