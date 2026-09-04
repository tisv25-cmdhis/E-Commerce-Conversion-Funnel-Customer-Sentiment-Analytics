# pip install pandas nltk pyodbc sqlalchemy

import pandas as pd
import nltk
from sqlalchemy import create_engine
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# NLTK Lexicon Download
nltk.download('vader_lexicon', quiet=True)

def fetch_data_from_sql():
    # SQLAlchemy engine to prevent Pandas UserWarning
    engine = create_engine(
        "mssql+pyodbc://V\\SQLEXPRESS/MarketingAnalytics"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
        "&TrustServerCertificate=yes"
    )
    
    query = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM dbo.customer_reviews"
    df = pd.read_sql(query, engine)
    return df

# Fetch data
customer_reviews_df = fetch_data_from_sql()

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def calculate_sentiment(review):
    if pd.isna(review):
        return 0.0
    sentiment = sia.polarity_scores(str(review))
    return sentiment['compound']

def categorize_sentiment(score, rating):
    if score > 0.05:
        if rating >= 4:
            return 'Positive'
        elif rating == 3:
            return 'Mixed Positive'
        else:
            return 'Mixed Negative'
    elif score < -0.05:
        if rating <= 2:
            return 'Negative'
        elif rating == 3:
            return 'Mixed Negative'
        else:
            return 'Mixed Positive'
    else:
        if rating >= 4:
            return 'Positive'
        elif rating <= 2:
            return 'Negative'
        else:
            return 'Neutral'

def sentiment_bucket(score):
    if score >= 0.5:
        return '0.5 to 1.0'
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'
    else:
        return '-1.0 to -0.5'

# Apply sentiment analysis
customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)

customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis=1)

customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_bucket)

# Print first 5 rows
print(customer_reviews_df.head())

# Export to CSV
customer_reviews_df.to_csv('customer_reviews_with_sentiment.csv', index=False)