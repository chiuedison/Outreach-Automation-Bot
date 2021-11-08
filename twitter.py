import os
from dotenv import load_dotenv
import tweepy


def create_api():
    ''' Creates and authenticates Twitter API'''
    # Load environment variables
    load_dotenv()
    # Twitter API credentials
    auth = tweepy.OAuthHandler(
        os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_KEY_SECRET'))
    auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'),
                          os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
    return tweepy.API(auth)


def send_dms(api):
    ''' Sends a direct message to the user '''
    # Get the user's ID
    id = api.get_user(screen_name='@ninja').id
    # Send the message
    api.send_direct_message(id, 'Hello!')


if __name__ == "__main__":
    api = create_api()
    send_dms(api)
