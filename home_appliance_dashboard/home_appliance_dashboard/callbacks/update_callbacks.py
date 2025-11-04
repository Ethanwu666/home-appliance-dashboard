import numpy as np
import pandas as pd
from dash import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# synthesize a 90-day price history around current price
def synthesize_price_history(current_price, days=90, seed=None):
    if seed is not None:
        np.random.seed(seed)
    base = float(current_price) if not pd.isna(current_price) else 20.0
    dates = [datetime.today() - timedelta(days=(days - 1 - i)) for i in range(days)]
    
    trend = np.linspace(base * 1.05, base * 0.95, days)
    noise = np.random.normal(0, base * 0.03, size=days)
    prices = trend + noise
    for _ in range(max(1, days // 30)):
        idx = np.random.randint(0, days)
        drop = prices[idx] * (0.12 + np.random.rand() * 0.2)
        prices[idx: idx + 2] = prices[idx: idx + 2] - drop
    prices = np.clip(prices, a_min=0.5, a_max=None)
    return pd.DataFrame({'date': dates, 'price': prices})

def normalize(x):
    x = np.array(x, dtype=float)
    if x.max() == x.min():
        return np.zeros_like(x)
    return (x - x.min()) / (x.max() - x.min())

def register_callbacks(app, df):
    @app.callback(
        Output('product-selector', 'value'),
        Input('top-search', 'value'),
        prevent_initial_call=False
    )
    def search_to_selector(q):
        if not q or str(q).strip() == "":
            return None
        q = q.strip()
        # find best match by substring in title
        mask = df['title'].str.contains(q, case=False, na=False)
        if mask.any():
            return df.loc[mask, 'asin'].iloc[0]
        return None

    #  update product info and all charts when product selected or product-selector changed
    @app.callback(
        Output('product-title', 'children'),
        Output('product-sub', 'children'),
        Output('product-price', 'children'),
        Output('product-savings', 'children'),
        Output('no-regret-badge', 'children'),
        Output('price-line-chart', 'figure'),
        Output('kpi-lowest', 'children'),
        Output('kpi-avg', 'children'),
        Output('kpi-vol', 'children'),
        Output('kpi-return', 'children'),
        Output('sentiment-histogram', 'figure'),
        Output('risk-radar', 'figure'),
        Output('comp-official', 'children'),
        Output('comp-jd', 'children'),
        Output('comp-suning', 'children'),
        Output('comp-tmall', 'children'),
        Input('product-selector', 'value'),
        Input('top-search', 'value'),
        State('product-selector', 'options'),
        prevent_initial_call=False
    )
    def update_product(asin, top_search, options):
        # Determine selected asin: priority selector->top_search match
        selected_asin = asin
        if (not selected_asin or pd.isna(selected_asin)) and top_search:
            mask = df['title'].str.contains(str(top_search), case=False, na=False)
            if mask.any():
                selected_asin = df.loc[mask, 'asin'].iloc[0]

        # choose first product
        if not selected_asin:
            row = df.iloc[0]
        else:
            row = df[df['asin'] == selected_asin]
            if row.empty:
                row = df.iloc[0]
            else:
                row = row.iloc[0]

        # Basic product fields
        title = row.get('title', 'Unknown Product')
        brand = row.get('brand', '')
        price_val = row.get('price/value', np.nan)
        price_str = f"${price_val:.2f}" if not pd.isna(price_val) else "N/A"
        # Sub text (SKU / rating)
        stars = row.get('stars', '')
        reviews = int(row.get('reviewsCount', 0)) if not pd.isna(row.get('reviewsCount', 0)) else 0
        sub = f"Brand: {brand} · Rating: {stars} · Reviews: {reviews}"

        # Simulate "was" price and savings if applicable (just sample)
        was_price = price_val * (1.2) if not pd.isna(price_val) else np.nan
        savings = f"Save ${was_price - price_val:.2f}" if (not pd.isna(price_val) and not pd.isna(was_price)) else ""

        # Regret / lowest-in-year badge heuristic:
        cat = row.get('category', '')
        cat_prices = df[df['category'] == cat]['price/value'].dropna()
        badge_text = ""
        if not cat_prices.empty and not pd.isna(price_val):
            threshold = cat_prices.quantile(0.10)
            if price_val <= threshold:
                badge_text = "Lowest in 1 year — No Regret!"
            else:
             
                badge_text = ""

        # Generate synthetic price history and build price line figure (Element B)
        hist_df = synthesize_price_history(price_val, days=90, seed=hash(row['asin']) % 2**32)
        price_fig = px.line(hist_df, x='date', y='price', title='', labels={'price': 'Price', 'date': 'Date'})
        # mark sale points as markers where big dip occurred
        dips = hist_df['price'].rolling(3).min() < (hist_df['price'].rolling(30, min_periods=1).mean() * 0.88)
        price_fig.add_trace(go.Scatter(
            x=hist_df.loc[dips, 'date'],
            y=hist_df.loc[dips, 'price'],
            mode='markers+text',
            marker=dict(size=10, color='red'),
            text=['SALE'] * dips.sum(),
            textposition='top center',
            name='Promotions'
        ))

        # KPIs (Element D) — compute over category
        cat_df = df[df['category'] == cat]
        lowest = cat_df['price/value'].min() if not cat_df.empty else np.nan
        avg = cat_df['price/value'].mean() if not cat_df.empty else np.nan
        vol = hist_df['price'].std()  
        ret_rate = min(0.25, max(0.0, (1 - row.get('sentiment_score', 0)) * 0.2))  # proxy

        # Sentiment histogram (Element E) using description polarity distribution of category
        sent_series = cat_df['sentiment_score'].fillna(0)
        sent_fig = px.bar(
            x=['Positive','Neutral','Negative'],
            y=[
                (sent_series > 0.1).sum(),
                ((sent_series >= -0.1) & (sent_series <= 0.1)).sum(),
                (sent_series < -0.1).sum()
            ],
            labels={'x': 'Sentiment', 'y': 'Count'},
            title=''
        )

        # Radar chart (Element F) compute normalized metrics for this product vs category
        pv = hist_df['price'].std()  # product volatility
        neg_sent_rate = (cat_df['sentiment_score'] < -0.1).mean() if not cat_df.empty else 0
        low_rating = max(0, (5.0 - float(row.get('stars', 5))) / 5.0)
        high_reviews_norm = (row.get('reviewsCount', 0) / (cat_df['reviewsCount'].max() if not cat_df.empty else 1))
        metrics = [pv, neg_sent_rate, low_rating, high_reviews_norm, ret_rate]
        normed = normalize(metrics)
        categories = ['Price Volatility', 'Negative Sentiment', 'Low Ratings', 'High Reviews', 'Return/Complaint']

        radar_fig = go.Figure()
        radar_fig.add_trace(go.Scatterpolar(r=normed, theta=categories, fill='toself', name='Risk Radar'))
        radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False)

        # Competitor simulated prices 
        def sim_comp_price(base, delta_pct):
            if pd.isna(base): return "N/A"
            val = base * (1 + delta_pct)
            return f"${val:.2f}"

        comp_official = f"Official Website  {sim_comp_price(price_val, -0.05)}"
        comp_jd = f"JD.com  {sim_comp_price(price_val, 0.07)}"
        comp_suning = f"Suning  {sim_comp_price(price_val, 0.25)}"
        comp_tmall = f"Tmall Official  {sim_comp_price(price_val, 0.25)}"

        # Format KPI strings
        kpi_low_s = f"${lowest:.2f}" if not pd.isna(lowest) else "N/A"
        kpi_avg_s = f"${avg:.2f}" if not pd.isna(avg) else "N/A"
        kpi_vol_s = f"{vol:.2f}"
        kpi_ret_s = f"{int(ret_rate * 100)}%"

        return (
            title,
            sub,
            price_str,
            savings,
            badge_text,
            price_fig,
            kpi_low_s,
            kpi_avg_s,
            kpi_vol_s,
            kpi_ret_s,
            sent_fig,
            radar_fig,
            comp_official,
            comp_jd,
            comp_suning,
            comp_tmall
        )
