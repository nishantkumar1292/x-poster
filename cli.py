#!/usr/bin/env python3
import os
import sys
import tweepy
from dotenv import load_dotenv


def main():
    # Load environment variables
    load_dotenv()

    # Twitter API credentials
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    # Check if credentials are available
    if not bearer_token:
        print("Error: Twitter Bearer Token is missing from .env file")
        sys.exit(1)

    # Get tweet content from command line args or prompt
    if len(sys.argv) > 1:
        tweet_content = " ".join(sys.argv[1:])
    else:
        print("Enter your post (press Enter twice to submit):")
        lines = []
        while True:
            line = input()
            if not line and lines:
                break
            lines.append(line)
        tweet_content = "\n".join(lines)

    # Check if content is provided
    if not tweet_content:
        print("Error: No content provided for posting")
        sys.exit(1)

    # Check character limit
    if len(tweet_content) > 280:
        print(
            f"Error: Your post exceeds the 280 character limit (current: {len(tweet_content)})"
        )
        sys.exit(1)

    try:
        # Initialize Twitter API v2
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        # Post to Twitter using v2 endpoint
        response = client.create_tweet(text=tweet_content)
        print(f"Successfully posted to X.com! Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"Error posting to X.com: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
