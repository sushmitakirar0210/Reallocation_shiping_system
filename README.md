Markdown
# 🍬 Nassau Candy Decision Intelligence & Shipping Reallocation System

An enterprise decision-support and supply chain optimization platform built with **Streamlit**, **Pandas**, and **Scikit-learn**. This platform optimizes fulfillment facility routing across North American manufacturing nodes to minimize delivery latency while preserving gross profit margins.

---

## 📋 Project Overview

The **Nassau Candy Decision Intelligence System** calculates real-time trade-offs between delivery velocity (transit lead time) and operational cost structures (unit profit margin erosion). 

By leveraging Haversine geographic mapping, multi-objective trade-off scoring, and a predictive machine learning engine, the platform enables logistics and supply chain teams to identify optimal manufacturing or fulfillment facilities for specific catalog products, customer delivery corridors, and contracted shipping modes.

---

## 🛠️ Repository**** Structure

```text
Reallocation_shipping_system/
├── app.py                      # Main Streamlit entrance workspace & Master Control Panel
├── data_engine.py              # Data ingestion engine & synthetic order ledger generator
├── model_pipeline.py           # Scikit-learn Gradient Boosting machine learning pipeline
├── nassau_candy_orders.csv     # Ingested historical shipping records ledger
├── requirements.txt            # Python dependencies
├── README.md                   # System documentation
└── pages/
    ├── Recommendations.py      # Strategic facility ranking & primary allocation decision
    ├── Risk_Panel.py           # Logistical safety guardrails & margin erosion log
    ├── Simulator.py            # Latency simulation bar charts & factual record lookup
    └── What_If.py              # Baseline vs. proposed realignment & weight sensitivity grid


#✨ Key Functional Modules
🎯 Master Control Engine (app.py): Configures priority weight allocations, calculates Haversine distance matrices, and executes dynamic multi-objective utility scoring.

📊 Factory Optimization Simulator (pages/Simulator.py): Visualizes candidate facility lead-time predictions alongside historical order records filtered by product and region.

🔄 What-If Scenario Analysis Matrix (pages/What_If.py): Compares legacy facility assignments against proposed realignments and runs sensitivity matrix grids across varying priority weights.

📋 Recommendation Dashboard (pages/Recommendations.py): Provides actionable allocation decisions and suitability rankings for candidate production nodes.

⚠️ Risk & Impact Guardrails (pages/Risk_Panel.py): Monitors operational safety thresholds, cross-hauling mileage limits, and fiscal margin erosion warnings.

🤖 Predictive Machine Learning Core (model_pipeline.py): Employs Scikit-learn's GradientBoostingRegressor, RobustScaler, and OneHotEncoder to predict fulfillment lead times.

🚀 Getting Started
1. Prerequisites
Ensure you have Python 3.10+ installed on your machine.

2. Installation
Clone this repository and install the required dependencies:

Bash
git clone [https://github.com/sushmitakirar0210/Reallocation_shipping_system.git](https://github.com/sushmitakirar0210/Reallocation_shipping_system.git)
cd Reallocation_shipping_system
pip install -r requirements.txt
3. Generate Historical Dataset
Generate the historical shipping dataset (nassau_candy_orders.csv):

Bash
python data_engine.py
4. Run the Application
Launch the Streamlit interactive dashboard:

Bash
streamlit run app.py
The application will automatically open in your default browser at http://localhost:8501.

🧰 Tech Stack
Frontend & Interactive UI: Streamlit

Data Manipulation & Analysis: Pandas, NumPy

Machine Learning Pipeline: Scikit-learn (GradientBoostingRegressor, OneHotEncoder, RobustScaler)

Visualization: Streamlit Native Charts, Plotly
