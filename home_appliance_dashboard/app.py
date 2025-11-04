import os
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from modules.data_processing import load_and_preprocess_data
from modules.layout import create_layout
from callbacks.update_callbacks import register_callbacks

# ---------------------------
# App
# ---------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Kitchenware Dashboard"

# very important for gunicorn
server = app.server

# ---------------------------
# Data (use absolute path based on this file)
# ---------------------------
HERE = Path(__file__).resolve().parent
DATA_FILE = HERE / "data" / "amazon_kitchenware.csv"
df = load_and_preprocess_data(str(DATA_FILE))

# ---------------------------
# Layout & Callbacks
# ---------------------------
app.layout = create_layout(df)
register_callbacks(app, df)

# ---------------------------
# Local dev entry (Render/gunicorn won't run this branch)
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=True)
