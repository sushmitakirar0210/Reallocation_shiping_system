import streamlit as st

st.title("⚠️ Risk & Impact Panel Log Guardrails")
st.markdown("---")

if "matrix_sim_records" not in st.session_state:
    st.warning("⚠️ No active optimization session found. Please run parameters from the main panel first.")
    st.stop()

current_legacy_factory = st.session_state.get("current_legacy_factory", "N/A")
absolute_optimum_factory = st.session_state.get("absolute_optimum_factory", "N/A")
legacy_metrics = st.session_state.get("legacy_metrics", {})
optimal_metrics = st.session_state.get("optimal_metrics", {})
weight_profit = st.session_state.get("weight_profit", 0.5)
weight_speed = st.session_state.get("weight_speed", 0.5)

if current_legacy_factory == absolute_optimum_factory:
    st.success(f"✅ Safe Horizon Profile: Under your current slider balance allocation metrics (Profit Focus: {weight_profit:.2f}), no systemic risk or fiscal margin leakage loops are triggered by assignment rules.")
else:
    margin_check = optimal_metrics.get("Margin Delta ($)", 0.0) - legacy_metrics.get("Margin Delta ($)", 0.0)
    if margin_check < 0:
        st.error(f"⚠️ HIGH-RISK MARGIN EROSION NOTICE ALIGNED: Your configuration weights favor transit speed over unit profitability ({weight_speed:.2f} speed focus). Moving volume to [{absolute_optimum_factory}] shortens timelines but erodes gross margin performance structures by ${abs(margin_check):.2f} per scale unit.")
    else:
        st.success("💡 REALIGNMENT SECURITY POLICY CLEARANCE LEVEL APPROVED: Allocation adjustment presents zero bottom-line volatility index threat markers.")

st.subheader("Automated Core Logistical Guardrails Monitor System Logs")
if optimal_metrics.get("Distance (km)", 0) > 2400:
    st.warning(f"🚨 Cross-Hauling Mileage Boundary Breach: Optimal facility target [{absolute_optimum_factory}] exceeds continental distance radius threshold rules.")
else:
    st.caption("✔ Proximity Mileage Radius Assessment Matrix: Route mileage dimensions conform to baseline freight target values.")

if abs(optimal_metrics.get("Margin Delta ($)", 0)) > 25.0:
    st.error("🚨 Fiscal Budget Line Variance Ceiling Breach: Delta exceeds acceptable variance boundaries.")
else:
    st.caption("✔ Budget Margin Friction Assessment Matrix: Projected cost variances reside inside safety threshold boundaries.")