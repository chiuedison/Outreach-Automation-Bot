import os
from dotenv import load_dotenv
import tweepy
from pyairtable import Table


class TwitterBot():
    ''' A Twitter bot that sends a message to the user '''

    def __init__(self, base_id, table_name):
        # Load environment variables
        load_dotenv()
        self.twitter_api = self.create_twitter_api()
        self.airtable_api = self.create_airtable_api(base_id, table_name)

    def create_twitter_api(self):
        ''' Creates and authenticates Twitter API'''
        # Twitter API credentials
        auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_KEY_SECRET'))
        auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'),
                              os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
        return tweepy.API(auth)

    def send_dms(self):
        ''' Sends a direct message to the user '''
        # Get the user's ID
        id = self.twitter_api.get_user(screen_name='@ninja').id
        # Send the message
        self.twitter_api.send_direct_message(id, 'Hello!')

    def create_airtable_api(self, base_id, table_name):
        ''' Creates and authenticates Airtable API'''
        # Airtable API credentials
        return Table(os.getenv('AIRTABLE_API_KEY'), base_id, table_name)


if __name__ == "__main__":
    bot = TwitterBot(base_id="appI43QnVsnxN3yYQ", table_name="Streamers")
    bot.send_dms()
