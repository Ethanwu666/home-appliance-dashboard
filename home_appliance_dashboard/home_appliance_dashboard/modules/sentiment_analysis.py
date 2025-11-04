from textblob import TextBlob

def compute_sentiment(text):
    if not text:
        return 0
    return TextBlob(text).sentiment.polarity

def keyword_counts(texts, keywords):
    counts = {k: 0 for k in keywords}
    for text in texts:
        for k in keywords:
            if k.lower() in text.lower():
                counts[k] += 1
    return counts
