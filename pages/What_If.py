import streamlit as st

st.title("🔄 What-If Scenario Analysis Matrix")
st.markdown("---")

if "matrix_sim_records" not in st.session_state:
    st.warning("⚠️ No active scenario context found. Please run parameters in the main panel first.")
    st.stop()

current_legacy_factory = st.session_state.get("current_legacy_factory", "N/A")
absolute_optimum_factory = st.session_state.get("absolute_optimum_factory", "N/A")
legacy_metrics = st.session_state.get("legacy_metrics", {})
optimal_metrics = st.session_state.get("optimal_metrics", {})
matrix_sim_records = st.session_state.get("matrix_sim_records", [])

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown("#### Baseline Rule Configuration (Legacy)")
    st.error(f"🏢 Factory: {current_legacy_factory}")
    st.metric("Timeline Transit Window Delay", f"{legacy_metrics.get('Predicted Lead Time (Days)', 0.0):.2f} Days")
    st.metric("Calculated Matrix Radius Distance", f"{legacy_metrics.get('Distance (km)', 0.0):,.1f} km")

with col_b2:
    st.markdown("#### Proposed Realignment Matrix Configuration")
    st.success(f"🏢 Factory: {absolute_optimum_factory}")
    lead_time_delta = optimal_metrics.get("Predicted Lead Time (Days)", 0.0) - legacy_metrics.get("Predicted Lead Time (Days)", 0.0)
    st.metric(
        "Expected Optimized Transit Window Delay",
        f"{optimal_metrics.get('Predicted Lead Time (Days)', 0.0):.2f} Days",
        delta=f"{lead_time_delta:.2f} Days",
        delta_color="inverse"
    )
    st.metric("Calculated Matrix Radius Distance", f"{optimal_metrics.get('Distance (km)', 0.0):,.1f} km")

st.markdown("---")
st.subheader("Weight Parameter Matrix Optimization Slider Sensitivity Log Grid")

sensitivity_list = []
for w_p in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    w_s = 1.0 - w_p
    best_fac_temp = current_legacy_factory
    best_score_temp = float("inf")
    for x in matrix_sim_records:
        score = (x["Predicted Lead Time (Days)"] * w_s * 15.0) + (abs(x["Margin Delta ($)"]) * w_p * 6.5)
        if score < best_score_temp:
            best_score_temp = score
            best_fac_temp = x["Factory"]
    sensitivity_list.append({
        "Financial Margin Weight": f"{w_p:.1f}",
        "Operational Transit Velocity Focus": f"{round(w_s, 1):.1f}",
        "Calculated Optimal Target Node Asset": best_fac_temp
    })

st.table(sensitivity_list)