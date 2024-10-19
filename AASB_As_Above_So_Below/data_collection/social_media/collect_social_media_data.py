# collect_social_media_data.py

import pandas as pd
import tweepy
import nltk
from datetime import datetime, timedelta
import sys

def collect_social_media_data(start_date, end_date, consumer_key, consumer_secret, access_token, access_token_secret):
    """
    Collects social media sentiment data from Twitter using Tweepy.
    
    Social media sentiment can drive investor behavior, influence market volatility,
    and serve as a real-time indicator of public reaction to news events, corporate actions,
    or economic policies.

    Parameters:
    - start_date (str): The start date for data collection in 'YYYY-MM-DD' format.
    - end_date (str): The end date for data collection in 'YYYY-MM-DD' format.
    - consumer_key (str): Your Twitter API consumer key.
    - consumer_secret (str): Your Twitter API consumer secret.
    - access_token (str): Your Twitter API access token.
    - access_token_secret (str): Your Twitter API access token secret.

    Returns:
    - df_social_sentiment (DataFrame): A pandas DataFrame containing dates and average sentiment scores.
    """

    # Authenticate with the Twitter API
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Initialize NLTK VADER sentiment analyzer
    nltk.download('vader_lexicon', quiet=True)
    sia = nltk.sentiment.vader.SentimentIntensityAnalyzer()

    # Define search parameters
    query = 'finance OR economy OR stock market OR investing OR trading'
    since_date = datetime.strptime(start_date, '%Y-%m-%d')
    until_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Create a list to store tweets and sentiments
    data = []

    # Twitter API limits the number of tweets per request and per time window
    # Use pagination and date ranges to collect tweets over the desired period

    current_date = since_date
    while current_date <= until_date:
        next_date = current_date + timedelta(days=1)
        try:
            tweets = tweepy.Cursor(api.search_tweets,
                                   q=query,
                                   lang='en',
                                   since=current_date.strftime('%Y-%m-%d'),
                                   until=next_date.strftime('%Y-%m-%d'),
                                   tweet_mode='extended').items(100)  # Adjust number of tweets as needed

            for tweet in tweets:
                if hasattr(tweet, 'full_text'):
                    text = tweet.full_text
                else:
                    text = tweet.text
                sentiment_score = sia.polarity_scores(text)['compound']
                data.append({'date': current_date.date(), 'sentiment': sentiment_score})
            print(f'Collected tweets for {current_date.strftime("%Y-%m-%d")}')
        except Exception as e:
            print(f'Error collecting tweets for {current_date.strftime("%Y-%m-%d")}: {e}')
            continue

        current_date = next_date

    if data:
        df_tweets = pd.DataFrame(data)
        # Group by date and calculate average sentiment
        df_social_sentiment = df_tweets.groupby('date')['sentiment'].mean().reset_index()
        print('Collected social media sentiment data')
    else:
        df_social_sentiment = pd.DataFrame(columns=['date', 'sentiment'])
        print('No social media sentiment data was collected.')

    return df_social_sentiment

def save_to_csv(df, filename):
    """
    Saves the DataFrame to a CSV file.

    Parameters:
    - df (DataFrame): The pandas DataFrame to save.
    - filename (str): The filename for the CSV file.
    """
    try:
        df.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to {filename}: {e}")

if __name__ == "__main__":
    # Configuration Parameters
    START_DATE = '2023-01-01'
    END_DATE = '2023-12-31'
    
    # Twitter API Credentials
    CONSUMER_KEY = 'Iix8fzImzGsDy45oud8WRsnG5'           # Replace with your actual Consumer Key
    CONSUMER_SECRET = '2skDUWEQBFVV3S3AEya6pgFnDfTTjPbRIW9kYVk8xczfWZiHAE'  # Replace with your actual Consumer Secret
    ACCESS_TOKEN = '1829183295218749440-cd7BKjL1opHZt6hLyo4N6sI81nvnfu'             # Replace with your actual Access Token
    ACCESS_TOKEN_SECRET = 'h4qxm3GRkOamfTMpjwaMDzsOHbYlzqRzsZwB3kc5QtH24'  # Replace with your actual Access Token Secret

    # Verify that all credentials are provided
    if not all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("Error: One or more Twitter API credentials are missing.")
        sys.exit(1)

    print("=== Fetching Social Media Sentiment Data ===")
    social_sentiment_df = collect_social_media_data(
        start_date=START_DATE,
        end_date=END_DATE,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    print(social_sentiment_df.head())
    save_to_csv(social_sentiment_df, 'social_media_sentiment.csv')