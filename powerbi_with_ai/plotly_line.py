# Re-initialize the environment and regenerate the dataset and visualization script.

import pandas as pd
import plotly.graph_objects as go

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

df = pd.DataFrame(data)

# Save dataset
file_path = "monthly_revenue_trends.csv"
df.to_csv(file_path, index=False)

# Plotly visualization with intersection highlights
regions = df["Region"].unique()

# Update the chart with improved colors and conditional color changes
# Initialize the figure
fig = go.Figure()

# Define basic colors for each region
region_colors = {"North America": "blue", "Asia": "red", "Europe": "orange"}

# Plotting the lines for each region
for region in regions:
    region_data = df[df["Region"] == region]

    if region == "Europe":
        # Check if Europe’s revenue goes below Asia’s revenue in any month
        for i, month in enumerate(region_data["Month"]):
            europe_revenue = region_data.iloc[i]["Revenue"]
            asia_revenue = df[(df["Region"] == "Asia") & (df["Month"] == month)][
                "Revenue"
            ].values[0]

            if europe_revenue < asia_revenue:
                region_colors["Europe"] = (
                    "black"  # Change Europe's color to black for all months
                )
                break  # Stop further checks once the color is changed

    fig.add_trace(
        go.Scatter(
            x=region_data["Month"],
            y=region_data["Revenue"],
            mode="lines+markers",
            name=region,
            line=dict(color=region_colors[region], width=2),
            marker=dict(size=8),
        )
    )

# Update layout for better visuals
fig.update_layout(
    title="Monthly Revenue Trends with Conditional Coloring for Europe",
    xaxis_title="Month",
    yaxis_title="Revenue (in Units)",
    legend_title="Region",
    template="plotly_white",
    xaxis=dict(tickmode="array", tickvals=df["Month"].unique()),
    font=dict(size=14),
)
# Save the chart
output_path = "monthly_revenue_trends_with_conditional_coloring.html"
fig.write_html(output_path)
