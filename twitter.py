import os
from dotenv import load_dotenv
import tweepy
from pyairtable import Table
from datetime import date


class TwitterBot():
    ''' A Twitter bot that sends messages to streamers on Twitter '''

    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.twitter_api = self.create_twitter_api()
        self.influencers_table = self.create_influencers_table(
            os.getenv('BASE_ID'), os.getenv('INFLUENCERS_TABLE_NAME'))
        self.params = self.get_params(
            os.getenv('BASE_ID'), os.getenv('PARAM_TABLE_NAME'))

    def create_twitter_api(self):
        ''' Creates and authenticates Twitter API'''
        # Twitter API credentials
        auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_KEY_SECRET'))
        auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'),
                              os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
        return tweepy.API(auth)

    def create_influencers_table(self, base_id, table_name):
        ''' Returns Airtable table that contains infromation about influencers '''
        # Airtable API credentials
        return Table(os.getenv('AIRTABLE_API_KEY'), base_id, table_name)

    def get_params(self, base_id, table_name):
        ''' Returns bot parameters pulled from Airtable '''
        # Airtable API credentials
        return Table(os.getenv('AIRTABLE_API_KEY'), base_id, table_name).all()[0]['fields']

    def send_dm(self, user):
        ''' Send a direct message to a user '''
        if (user['fields']['Ranking (0 - 4)'] == 0 or user['fields']['Twitter Handle'][0] != '@'):
            return
        attempt_num = user['fields']['Number of attempts']
        if (attempt_num >= params['Number of messages']):
            # We already sent the max number of messages
            return
        if (attempt_num > 0):
            # Check the last date we sent a message
            pass
        handle = user['fields']['Twitter Handle']
        profile = self.twitter_api.get_user(screen_name=handle)
        link = self.params['Link']
        message = self.params['Message #' + str(attempt_num + 1)]
        try:
            self.twitter_api.send_direct_message(profile.id, message + link)
            self.influencers_table.update(
                user['id'], {'Number of attempts': attempt_num + 1})
            self.influencers_table.update(
                user['id'], {'Twitter DM blocked?': 'No'})
            self.influencers_table.update(user['id'], {'Last Twitter messages attempt': date.today().strftime(
                "%m/%d/%y")})
        except tweepy.errors.Forbidden:
            self.influencers_table.update(
                user['id'], {'Twitter DM blocked?': 'Yes'})

    def run(self):
        ''' Send messages to streamers on Twiiter '''
        # Get all users from Airtable
        users = self.influencers_table.all()
        for user in users:
            self.send_dm(user)


def main():
    bot = TwitterBot()
    bot.run()


if __name__ == "__main__":
    main()
