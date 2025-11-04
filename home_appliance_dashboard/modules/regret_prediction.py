def detect_high_risk(df):
    high_risk = df[df['sentiment_score'] < 0.2]
    if not high_risk.empty:
        return "High-risk products:\n" + ", ".join(high_risk['title'].head(5))
    else:
        return "No high-risk products detected."
