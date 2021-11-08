import os
from dotenv import load_dotenv
import tweepy

# Load environment variables
load_dotenv()

# Authenticate to Twitter
auth = tweepy.OAuthHandler(
    os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_KEY_SECRET'))
auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'),
                      os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
