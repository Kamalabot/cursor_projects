import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template_string, request

# Initialize Flask App
app = Flask(__name__)

# Create a more complex sample dataset
data = {
    "date": [
        "2025-01-01",
        "2025-01-02",
        "2025-01-03",
        "2025-01-04",
        "2025-01-01",
        "2025-01-02",
        "2025-01-03",
        "2025-01-04",
        "2025-01-01",
        "2025-01-02",
        "2025-01-03",
        "2025-01-04",
    ],
    "product_id": [
        "product_1",
        "product_1",
        "product_1",
        "product_1",
        "product_2",
        "product_2",
        "product_2",
        "product_2",
        "product_3",
        "product_3",
        "product_3",
        "product_3",
    ],
    "category_id": [
        "cat_1",
        "cat_1",
        "cat_1",
        "cat_1",
        "cat_2",
        "cat_2",
        "cat_2",
        "cat_2",
        "cat_3",
        "cat_3",
        "cat_3",
        "cat_3",
    ],
    "region_id": [
        "region_1",
        "region_1",
        "region_1",
        "region_1",
        "region_1",
        "region_1",
        "region_1",
        "region_1",
        "region_2",
        "region_2",
        "region_2",
        "region_2",
    ],
    "sales": [10, 15, 20, 10, 5, 10, 8, 12, 7, 13, 14, 9],
}

# Load the data into a DataFrame
df = pd.DataFrame(data)


@app.route("/")
def stream_sales_data():
    # Get product_id, category_id, and region_id as query parameters (defaults provided)
    product_id = request.args.get("product_id", default="product_1", type=str)
    category_id = request.args.get("category_id", default="cat_1", type=str)
    region_id = request.args.get("region_id", default="region_1", type=str)

    # Filter the data for the selected product, category, and region
    filtered_data = df[
        (df["product_id"] == product_id)
        & (df["category_id"] == category_id)
        & (df["region_id"] == region_id)
    ]

    # Create a bar chart using Plotly
    fig = px.bar(
        filtered_data,
        x="date",
        y="sales",
        title=f"Sales for {product_id} in {category_id} ({region_id})",
    )

    # Convert the plotly figure to HTML
    graph_html = pio.to_html(fig, full_html=False)

    return render_template_string(
        "<html><body>{{ graph_html | safe }}</body></html>", graph_html=graph_html
    )


if __name__ == "__main__":
    app.run(debug=True)
