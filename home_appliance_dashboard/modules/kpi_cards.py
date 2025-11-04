import dash_bootstrap_components as dbc
from dash import html

def create_kpi_cards(df):
    #  initial values can be computed or 0
    lowest = df['price/value'].min()
    avg_price = round(df['price/value'].mean(), 2)
    volatility = round(df['price/value'].std(), 2)
    avg_sentiment = round(df['sentiment_score'].mean(), 2)
    
    row = dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Lowest Price"),
            html.H3(f"${lowest}", id='lowest-price')   
        ])), width=3),
        
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Average Price"),
            html.H3(f"${avg_price}", id='avg-price')  
        ])), width=3),
        
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Price Volatility"),
            html.H3(f"{volatility}", id='volatility')  
        ])), width=3),
        
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Average Sentiment"),
            html.H3(f"{avg_sentiment}", id='avg-sentiment')  
        ])), width=3),
    ])
    
    return row
