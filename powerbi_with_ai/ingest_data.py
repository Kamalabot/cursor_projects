import pandas as pd

# Create sample data
data = {
    "Month": [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    * 3,  # Repeat for each region
    "Region": (["North America"] * 12 + ["Europe"] * 12 + ["Asia"] * 12),
    "Revenue": [
        200,
        220,
        250,
        270,
        300,
        330,
        360,
        390,
        420,
        450,
        480,
        500,  # North America
        150,
        160,
        170,
        180,
        200,
        210,
        230,
        250,
        270,
        290,
        310,
        330,  # Europe
        100,
        120,
        140,
        160,
        180,
        200,
        230,
        260,
        290,
        310,
        330,
        350,  # Asia
    ],
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save dataset to CSV
df.to_csv("monthly_revenue_trends.csv", index=False)

print(df.head(4))  # Display the first 12 rows
