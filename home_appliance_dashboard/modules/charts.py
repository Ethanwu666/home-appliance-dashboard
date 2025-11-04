import plotly.express as px
import plotly.graph_objects as go

def create_price_chart(df):
    #  ASIN as x-axis, keep full title in hover
    return px.line(df, x='asin', y='price/value', 
                   hover_data=['title'], 
                   title='Price Trend')

def create_sentiment_histogram(df):
    return px.histogram(df, x='sentiment_score', nbins=20, title='Sentiment Distribution')

def create_category_histogram(df):
    return px.histogram(df, x='category', title='Products per Category')

def create_comparison_chart(df):
    return px.scatter(df, x='price/value', y='stars', size='reviewsCount',
                      hover_data=['title', 'brand'], title='Product Comparison')

def create_radar_chart(df):
    categories = ['Price Volatility', 'Negative Sentiment', 'Low Ratings', 'High Reviews']
    risks = [
        df['price_volatility'].mean()/df['price/value'].max(),
        1 - df['sentiment_score'].mean(),
        5 - df['stars'].mean(),
        df['reviewsCount'].mean()/df['reviewsCount'].max()
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=risks, theta=categories, fill='toself', name='Risk Radar'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])), showlegend=False)
    return fig
