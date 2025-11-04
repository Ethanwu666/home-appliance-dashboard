import pandas as pd
from textblob import TextBlob

def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    
    # Price as float
    df['price/value'] = pd.to_numeric(df['price/value'], errors='coerce')
    
    # Sentiment score
    df['sentiment_score'] = df['description'].fillna("").apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    
    # Category extraction
    df['category'] = df['breadCrumbs'].apply(lambda x: str(x).split('›')[-1].strip())
    
    # Price volatility (rolling std as placeholder)
    df['price_volatility'] = df['price/value'].rolling(5, min_periods=1).std()
    
    return df
