import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from modules.data_processing import load_and_preprocess_data
from modules.layout import create_layout
from callbacks.update_callbacks import register_callbacks

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Kitchenware Dashboard"

# Load data
df = load_and_preprocess_data('data/amazon_kitchenware.csv')

# Layout
app.layout = create_layout(df)

# Callbacks
register_callbacks(app, df)

# Run
if __name__ == "__main__":
    app.run(debug=True)
