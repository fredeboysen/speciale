import requests
import json
import csv
import re
import os
from dotenv import load_dotenv

# Define API details
url = "https://twitter241.p.rapidapi.com/search-v2"

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

headers = {
    "x-rapidapi-host": "twitter241.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY  # Securely loaded
}

# Define query parameters
query_params = {
    "type": "Latest",  # Fetch latest tweets
    "count": 20,       # Request 50 tweets
    "query": "$TSLA$"
}

def contains_tsla_before_other_tickers(tweet_text):
    """
    Check if '$TSLA' appears in the main part of the tweet before any other stock tickers.
    """
    # Match all stock tickers (e.g., $AAPL, $TSLA, etc.)
    tickers = re.findall(r"\$[A-Z]+", tweet_text)

    if not tickers or "$TSLA" not in tickers:
        return False  # No stock tickers or TSLA is missing
    
    # Ensure TSLA is the first mentioned stock ticker
    return tickers[0] == "$TSLA"

# Make API request
response = requests.get(url, headers=headers, params=query_params)

if response.status_code == 200:
    try:
        tweets_data = response.json()

        # Navigate JSON structure
        timeline = tweets_data.get("result", {}).get("timeline", {}).get("instructions", [])

        tweets = []
        for instruction in timeline:
            if "entries" in instruction:
                for entry in instruction["entries"]:
                    content = entry.get("content", {})
                    tweet_info = content.get("itemContent", {}).get("tweet_results", {}).get("result", {})

                    # Extract tweet details
                    tweet_text = tweet_info.get("legacy", {}).get("full_text", "")
                    tweet_id = tweet_info.get("rest_id", "")
                    tweet_time = tweet_info.get("legacy", {}).get("created_at", "")
                    user = tweet_info.get("core", {}).get("user_results", {}).get("result", {}).get("legacy", {}).get("screen_name", "")

                    # Generate Tweet URL
                    tweet_url = f"https://x.com/{user}/status/{tweet_id}" if user and tweet_id else ""

                    # Apply stricter filtering: Only keep tweets where $TSLA is mentioned before any other ticker
                    if tweet_text and contains_tsla_before_other_tickers(tweet_text):
                        tweets.append([tweet_id, tweet_time, user, tweet_text, tweet_url])

        # Save to CSV
        with open("filtered_tweets_tsla.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Tweet_ID", "Timestamp", "Username", "Tweet_Text", "Tweet_URL"])
            writer.writerows(tweets)

        print(f"✅ Saved {len(tweets)} filtered tweets to filtered_tweets_tsla.csv")

    except json.JSONDecodeError:
        print("Failed to decode JSON. Possible API issue.")

else:
    print(f"Error: {response.status_code}, {response.text}")
