import requests

# Define API details
url = "https://twitter241.p.rapidapi.com/search-v2"

headers = {
    "x-rapidapi-host": "twitter241.p.rapidapi.com",
    "x-rapidapi-key": "6b22ffb88amshca0ce5cdc12a862p18b79fjsn417f8d2bf56b"
}

# Define query parameters
query_params = {
    "type": "Latest",  # Change to 'Latest' to get recent tweets
    "count": 10,       # Request 50 tweets
    "query": "$TSLA$"
}

# Make API request
response = requests.get(url, headers=headers, params=query_params)

# Check response
if response.status_code == 200:
    try:
        tweets_data = response.json()

        # Navigate the JSON structure to locate tweets
        timeline = tweets_data.get("result", {}).get("timeline", {}).get("instructions", [])

        tweets = []
        for instruction in timeline:
            if "entries" in instruction:
                for entry in instruction["entries"]:
                    content = entry.get("content", {})
                    tweet_info = content.get("itemContent", {}).get("tweet_results", {}).get("result", {})

                    # Extract tweet text
                    tweet_text = tweet_info.get("legacy", {}).get("full_text", "")
                    tweet_id = tweet_info.get("rest_id", "")
                    tweet_time = tweet_info.get("legacy", {}).get("created_at", "")
                    user = tweet_info.get("core", {}).get("user_results", {}).get("result", {}).get("legacy", {}).get("screen_name", "")

                    if tweet_text:
                        tweets.append(f"User: {user}\nTime: {tweet_time}\nTweet: {tweet_text}\nTweet ID: {tweet_id}\n")

        # Print the extracted tweets
        if tweets:
            for i, tweet in enumerate(tweets[:10]):  # Ensure max 50 tweets
                print(f"{i+1}. {tweet}\n")
        else:
            print("No tweets found.")

    except json.JSONDecodeError:
        print("Failed to decode JSON. Possible API issue.")

else:
    print(f"Error: {response.status_code}, {response.text}")
