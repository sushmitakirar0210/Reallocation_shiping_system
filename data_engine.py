from datetime import datetime, timedelta
import numpy as np
import pandas as pd

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

def generate_historical_ledger(records: int = 10000) -> pd.DataFrame:
    np.random.seed(42)
    products = list(PRODUCT_REGISTRY.keys())
    regions = ["Atlantic", "Gulf", "Interior", "Pacific"]
    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
    base_date = datetime(2023, 1, 1)

    data = []
    for i in range(records):
        prod = str(np.random.choice(products))
        region = str(np.random.choice(regions))
        ship_mode = str(np.random.choice(ship_modes))

        sales = float(np.round(np.random.exponential(scale=600) + 40, 2))
        units = int(np.random.randint(2, 80))
        cost = float(np.round(sales * np.random.uniform(0.50, 0.70), 2))
        gross_profit = float(np.round(sales - cost, 2))

        base_days = {"Standard Class": 6, "Second Class": 4, "First Class": 2, "Same Day": 0}[ship_mode]
        origin = PRODUCT_REGISTRY[prod]["Factory"]
        delay = 0.0
        if origin == "Lot's O' Nuts" and region == "Atlantic": delay += 3.5
        if origin == "Wicked Choccy's" and region == "Pacific": delay += 3.0
        if origin == "Sugar Shack" and region == "Gulf": delay += 2.0

        lead_time = int(base_days + delay + np.random.poisson(lam=1.0))
        order_date = base_date + timedelta(days=int(np.random.randint(0, 365)))
        ship_date = order_date + timedelta(days=lead_time)

        data.append([
            f"CA-2023-{100000 + i}",
            order_date.strftime("%d-%m-%Y"),
            ship_date.strftime("%d-%m-%Y"),
            region,
            PRODUCT_REGISTRY[prod]["Division"],
            prod,
            origin,
            ship_mode,
            sales,
            units,
            cost,
            gross_profit,
            lead_time
        ])

    cols = ["Order ID", "Order Date", "Ship Date", "Region", "Division", "Product Name", "Factory", "Ship Mode", "Sales", "Units", "Cost", "Gross Profit", "Lead Time"]
    return pd.DataFrame(data, columns=cols)

if __name__ == "__main__":
    df = generate_historical_ledger(10000)
    df.to_csv("nassau_candy_orders.csv", index=False)
    print("✅ Generated 'nassau_candy_orders.csv' with 10,000 records.")