import os
import tweepy
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

# Load environment variables
load_dotenv()

# Twitter API credentials
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")


# Initialize Twitter API v2 client
def get_twitter_client():
    return tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )


# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tweet_content = request.form.get("tweet_content")

        if not tweet_content:
            flash("Tweet content cannot be empty", "error")
            return redirect(url_for("index"))

        try:
            # Post the tweet using v2 API
            twitter_client = get_twitter_client()
            response = twitter_client.create_tweet(text=tweet_content)
            tweet_id = response.data["id"]
            flash(f"Tweet posted successfully! Tweet ID: {tweet_id}", "success")
        except Exception as e:
            flash(f"Error posting tweet: {str(e)}", "error")

        return redirect(url_for("index"))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
