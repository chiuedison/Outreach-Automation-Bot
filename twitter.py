import os
from dotenv import load_dotenv
import tweepy
from pyairtable import Table


class TwitterBot():
    ''' A Twitter bot that sends a message to the user '''

    def __init__(self, base_id, table_name, num_of_attempts):
        # Load environment variables
        load_dotenv()
        self.twitter_api = self.create_twitter_api()
        self.airtable_api = self.create_airtable_api(base_id, table_name)
        self.num_of_attempts = num_of_attempts

    def create_twitter_api(self):
        ''' Creates and authenticates Twitter API'''
        # Twitter API credentials
        auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_KEY_SECRET'))
        auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'),
                              os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
        return tweepy.API(auth)

    def create_airtable_api(self, base_id, table_name):
        ''' Creates and authenticates Airtable API'''
        # Airtable API credentials
        return Table(os.getenv('AIRTABLE_API_KEY'), base_id, table_name)

    def send_dms(self):
        ''' Sends a direct message to the user from AirTable'''
        # Get all users from Airtable
        users = self.airtable_api.all()
        num_twitter_handles = 0
        for user in users:
            if (user['fields']['Ranking (0 - 4)'] != 0 and user['fields']['Twitter Handle'][0] == '@'):
                if (user['fields']['# of attempts'] <= self.num_of_attempts):
                    print(user['fields']['Twitter Handle'])
                    num_twitter_handles += 1
            else:
                print('No Twitter Handle or 0 Ranking')
        print('Number of Twitter handles: ' + str(num_twitter_handles))


def main():
    base_id = "appI43QnVsnxN3yYQ"
    table_name = "Twitch Top 400- Ranked & Scored"
    num_of_attempts = 4
    bot = TwitterBot(base_id, table_name, num_of_attempts)
    bot.send_dms()


if __name__ == "__main__":
    main()
