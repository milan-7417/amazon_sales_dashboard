import pandas as pd
import numpy as np

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)
server = app.server



# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/cleaned_amazon_sales.csv")

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# Drop missing amount
df = df.dropna(subset=["Amount"])

# Fill missing values
df["Courier Status"] = df["Courier Status"].fillna("Unknown")
df["ship-state"] = df["ship-state"].fillna("Unknown")
df["Category"] = df["Category"].fillna("Unknown")
df["Fulfilment"] = df["Fulfilment"].fillna("Unknown")

# Sort dates
df = df.sort_values("Date")


# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_revenue = round(df["Amount"].sum(), 2)
total_orders = df["Order ID"].nunique()
total_qty = df["Qty"].sum()

avg_order_value = round(
    total_revenue / total_orders, 2
)

cancelled_orders = (
    df["Status"]
    .str.contains("Cancelled", case=False)
    .sum()
)

cancel_rate = round(
    (cancelled_orders / len(df)) * 100,
    2
)

top_category = (
    df.groupby("Category")["Amount"]
    .sum()
    .idxmax()
)



app.title = "Amazon Sales Dashboard"


# -----------------------------
# FILTER OPTIONS
# -----------------------------
states = sorted(
    df["ship-state"].dropna().unique()
)

categories = sorted(
    df["Category"].dropna().unique()
)

statuses = sorted(
    df["Status"].dropna().unique()
)

fulfilments = sorted(
    df["Fulfilment"].dropna().unique()
)


# -----------------------------
# LAYOUT
# -----------------------------
app.layout = html.Div(

    className="main-container",

    children=[

        html.H1(
            "Amazon Sales Analytics Dashboard",
            className="dashboard-title"
        ),

        # -------------------------
        # FILTERS
        # -------------------------
        html.Div(

            className="filter-container",

            children=[

                html.Div([
                    html.Label("State"),
                    dcc.Dropdown(
                        id="state-filter",
                        options=[
                            {
                                "label": s,
                                "value": s
                            }
                            for s in states
                        ],
                        multi=True,
                        placeholder="Select State",
                        searchable=True,
                        className="dropdown-fix",
                        optionHeight=40,
                        maxHeight=250,
                        closeOnSelect=False
                    )
                ]),

                html.Div([
                    html.Label("Category"),
                    dcc.Dropdown(
                        id="category-filter",
                        options=[
                            {
                                "label": c,
                                "value": c
                            }
                            for c in categories
                        ],
                        multi=True,
                        placeholder="Select Category",
                        searchable=True,
                        className="dropdown-fix",
                        optionHeight=40,
                        maxHeight=250,
                        closeOnSelect=False
                    )
                ]),

                html.Div([
                    html.Label("Status"),
                    dcc.Dropdown(
                        id="status-filter",
                        options=[
                            {
                                "label": s,
                                "value": s
                            }
                            for s in statuses
                        ],
                        multi=True,
                        placeholder="Select Status",
                        searchable=True,
                        className="dropdown-fix",
                        optionHeight=40,
                        maxHeight=250,
                        closeOnSelect=False 
                    )
                ]),

                html.Div([
                    html.Label("Fulfilment"),
                    dcc.Dropdown(
                        id="fulfilment-filter",
                        options=[
                            {
                                "label": f,
                                "value": f
                            }
                            for f in fulfilments
                        ],
                        multi=True,
                        placeholder="Select Fulfilment",
                        searchable=True,
                        className="dropdown-fix",
                        optionHeight=40,
                        maxHeight=250,
                        closeOnSelect=False
                    )
                ])

            ]
        ),

        # -------------------------
        # KPI CARDS
        # -------------------------
        html.Div(

            className="kpi-container",

            children=[

                html.Div([
                    html.H3("₹ {:,.0f}".format(total_revenue)),
                    html.P("Total Revenue")
                ], className="kpi-card"),

                html.Div([
                    html.H3("{:,}".format(total_orders)),
                    html.P("Total Orders")
                ], className="kpi-card"),

                html.Div([
                    html.H3("{:,}".format(total_qty)),
                    html.P("Total Quantity")
                ], className="kpi-card"),

                html.Div([
                    html.H3("₹ {:,.0f}".format(avg_order_value)),
                    html.P("Avg Order Value")
                ], className="kpi-card"),

                html.Div([
                    html.H3(f"{cancel_rate}%"),
                    html.P("Cancellation Rate")
                ], className="kpi-card"),

                html.Div([
                    html.H3(top_category),
                    html.P("Top Category")
                ], className="kpi-card")
            ]
        ),

        # -------------------------
        # CHARTS
        # -------------------------
        html.Div(

            className="chart-grid",

            children=[

                dcc.Graph(
                    id="sales-trend-chart"
                ),

                dcc.Graph(
                    id="status-chart"
                ),

                dcc.Graph(
                    id="state-chart"
                ),

                dcc.Graph(
                    id="category-chart"
                ),

                dcc.Graph(
                    id="courier-chart"
                ),

                dcc.Graph(
                    id="size-chart"
                )

            ]
        )
    ]
)

# -----------------------------
# CALLBACKS
# -----------------------------
@app.callback(
    [
        Output("sales-trend-chart", "figure"),
        Output("status-chart", "figure"),
        Output("state-chart", "figure"),
        Output("category-chart", "figure"),
        Output("courier-chart", "figure"),
        Output("size-chart", "figure"),
    ],
    [
        Input("state-filter", "value"),
        Input("category-filter", "value"),
        Input("status-filter", "value"),
        Input("fulfilment-filter", "value"),
    ]
)
def update_dashboard(
    selected_states,
    selected_categories,
    selected_status,
    selected_fulfilment
):

    filtered_df = df.copy()

    # -------------------------
    # FILTERING
    # -------------------------
    if selected_states:
        filtered_df = filtered_df[
            filtered_df["ship-state"]
            .isin(selected_states)
        ]

    if selected_categories:
        filtered_df = filtered_df[
            filtered_df["Category"]
            .isin(selected_categories)
        ]

    if selected_status:
        filtered_df = filtered_df[
            filtered_df["Status"]
            .isin(selected_status)
        ]

    if selected_fulfilment:
        filtered_df = filtered_df[
            filtered_df["Fulfilment"]
            .isin(selected_fulfilment)
        ]

    # -------------------------
    # SALES TREND
    # -------------------------

    sales_trend = (
    filtered_df
    .groupby("Month_num")["Amount"]
    .sum()
    .reset_index()
    )

    fig_sales = px.line(
    sales_trend,
    x="Month_num",
    y="Amount",
    markers=True,
    title="Monthly Revenue Trend"
    )

    fig_sales.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    height=450,
    xaxis_title="Month",
    yaxis_title="Revenue"
    )

    fig_sales.update_traces(
    line_color="#06b6d4",
    line_width=4
)

    # -------------------------
    # ORDER STATUS
    # -------------------------
    status_data = (
        filtered_df["Status"]
        .value_counts()
        .reset_index()
    )

    status_data.columns = [
        "Status",
        "Count"
    ]

    fig_status = px.pie(
        status_data,
        names="Status",
        values="Count",
        hole=0.55,
        title="Order Status Distribution"
    )

    fig_status.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        font_color="white",
        height=450
    )

    # -------------------------
    # TOP STATES
    # -------------------------
    state_data = (
        filtered_df
        .groupby("ship-state")["Amount"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()
    )

    fig_state = px.bar(
        state_data,
        x="Amount",
        y="ship-state",
        orientation="h",
        title="Top 10 States by Revenue"
    )

    fig_state.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        height=450
    )

    

    # -------------------------
    # CATEGORY SALES
    # -------------------------

    category_data = (
    filtered_df
    .groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    )

    fig_category = px.bar(
    category_data,
    x="Amount",
    y="Category",
    orientation="h",
    text_auto=".2s",
    title="Revenue by Category"
    )

    fig_category.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    height=450
    )

    fig_category.update_traces(
    marker_color="#8b5cf6"
    )

    # -------------------------
    # COURIER STATUS
    # -------------------------
    courier_data = (
        filtered_df[
            "Courier Status"
        ]
        .value_counts()
        .reset_index()
    )

    courier_data.columns = [
        "Courier Status",
        "Count"
    ]

    fig_courier = px.bar(
        courier_data,
        x="Courier Status",
        y="Count",
        title="Courier Performance"
    )

    fig_courier.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        height=450
    )

    # -------------------------
    # SIZE DEMAND
    # -------------------------
    size_data = (
        filtered_df["Size"]
        .value_counts()
        .reset_index()
    )

    size_data.columns = [
        "Size",
        "Count"
    ]

    fig_size = px.bar(
        size_data,
        x="Size",
        y="Count",
        title="Size Demand Analysis"
    )

    fig_size.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        height=450
    )

    return (
        fig_sales,
        fig_status,
        fig_state,
        fig_category,
        fig_courier,
        fig_size
    )


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False
    )
    