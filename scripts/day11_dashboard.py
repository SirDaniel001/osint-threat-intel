import os
import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px

# ✅ Fix dataset path for local + Docker
DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/unified_threat_dataset.csv")
if not os.path.exists(DATA_FILE):
    DATA_FILE = "/app/data/unified_threat_dataset.csv"

if not os.path.exists(DATA_FILE):
    raise FileNotFoundError("[ERROR] Unified dataset not found. Run day11_merge_datasets.py first.")

# ✅ Load Data
df = pd.read_csv(DATA_FILE)

# Ensure required columns exist
for col in ["source_type", "domain", "risk_score", "ioc_tags"]:
    if col not in df.columns:
        df[col] = ""

# ✅ Preprocess IOC Tags for Dropdown
unique_tags = sorted(set(sum([str(x).split(",") for x in df["ioc_tags"].dropna()], [])))

# ✅ Initialize Dash App
app = dash.Dash(__name__)
app.title = "OSINT Threat Intelligence Dashboard"

# ✅ Layout
app.layout = html.Div([
    html.H1("OSINT Threat Intelligence Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Filter by IOC Tags:"),
        dcc.Dropdown(
            id="ioc-filter",
            options=[{"label": t, "value": t} for t in unique_tags],
            multi=True,
            placeholder="Select IOC Tags"
        ),
        html.Label("Filter by Source Type:"),
        dcc.Dropdown(
            id="source-filter",
            options=[{"label": s, "value": s} for s in df["source_type"].dropna().unique()],
            multi=True,
            placeholder="Select Source Type"
        ),
        html.Label("Risk Score Range:"),
        dcc.RangeSlider(
            id="risk-slider",
            min=0, max=100, step=5,
            value=[0, 100],
            marks={i: str(i) for i in range(0, 101, 20)}
        ),
        html.Br(),
        html.Button("Download CSV", id="download-csv-btn"),
        dcc.Download(id="download-csv"),
        html.Button("Download JSON", id="download-json-btn"),
        dcc.Download(id="download-json"),
        html.Br(), html.Br(),
        html.Button("Toggle Dark Theme", id="theme-toggle", n_clicks=0)
    ], style={"width": "80%", "margin": "auto"}),

    html.Br(),

    html.Div([
        dcc.Graph(id="source-chart"),
        dcc.Graph(id="ioc-chart"),
        dcc.Graph(id="risk-chart")
    ]),

    html.Br(),

    html.H3("Unified Threat Intelligence Data"),
    dash_table.DataTable(
        id="data-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        page_size=10,
        style_table={"overflowX": "auto"}
    ),

    dcc.Interval(
        id="interval-refresh",
        interval=30 * 1000,  # Auto-refresh every 30s
        n_intervals=0
    )
], id="main-div")

# ✅ Callbacks

@app.callback(
    [Output("source-chart", "figure"),
     Output("ioc-chart", "figure"),
     Output("risk-chart", "figure"),
     Output("data-table", "data")],
    [Input("ioc-filter", "value"),
     Input("source-filter", "value"),
     Input("risk-slider", "value"),
     Input("interval-refresh", "n_intervals")]
)
def update_dashboard(selected_tags, selected_sources, risk_range, _):
    filtered = df.copy()

    if selected_tags:
        filtered = filtered[filtered["ioc_tags"].apply(lambda x: any(tag in str(x) for tag in selected_tags))]
    if selected_sources:
        filtered = filtered[filtered["source_type"].isin(selected_sources)]
    filtered = filtered[(filtered["risk_score"].fillna(0).astype(float) >= risk_range[0]) &
                         (filtered["risk_score"].fillna(0).astype(float) <= risk_range[1])]

    # Charts
    source_fig = px.histogram(filtered, x="source_type", title="Sources Distribution", color="source_type")
    ioc_fig = px.histogram(filtered, x="ioc_tags", title="IOC Tags Frequency")
    risk_fig = px.histogram(filtered, x="risk_score", nbins=20, title="Risk Score Distribution")

    return source_fig, ioc_fig, risk_fig, filtered.to_dict("records")

@app.callback(
    Output("download-csv", "data"),
    Input("download-csv-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_csv(_):
    return dcc.send_file(DATA_FILE)

@app.callback(
    Output("download-json", "data"),
    Input("download-json-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_json(_):
    json_file = DATA_FILE.replace(".csv", ".json")
    return dcc.send_file(json_file)

# ✅ Theme Toggle (CSS Switch)
@app.callback(
    Output("main-div", "style"),
    Input("theme-toggle", "n_clicks")
)
def toggle_theme(n):
    if n % 2 == 1:
        return {"backgroundColor": "#222", "color": "#fff", "padding": "10px"}
    return {"backgroundColor": "#fff", "color": "#000", "padding": "10px"}

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
