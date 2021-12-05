import os
from dotenv import load_dotenv
import tweepy
from pyairtable import Table
from time import sleep
from datetime import date


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

    def send_dm(self, handle, message_number, user):
        ''' Send a direct message to a user '''
        print(handle)
        profile = self.twitter_api.get_user(screen_name=handle)
        message = 'Hello ' + handle + '! I am a bot that will send you a message every day.'
        try:
            self.twitter_api.send_direct_message(profile.id, message)
            counter = user['fields']['# of attempts'] + 1
            self.airtable_api.update(user['id'], {'# of attempts': counter})
            self.airtable_api.update(user['id'], {'Twitter DM blocked?': 'No'})
            self.airtable_api.update(user['id'], {'Last Twitter messages attempt': date.today().strftime(
                "%m/%d/%y")})
        except tweepy.errors.Forbidden:
            self.airtable_api.update(
                user['id'], {'Twitter DM blocked?': 'Yes'})

    def run(self):
        ''' Send messages to streamers on Twiiter '''
        # Get all users from Airtable
        users = self.airtable_api.all()
        for user in users:
            if (user['fields']['Ranking (0 - 4)'] != 0 and user['fields']['Twitter Handle'][0] == '@'):
                if (user['fields']['# of attempts'] == 0):
                    # send initial message
                    pass
                elif (user['fields']['# of attempts'] == 1):
                    # send follow up message (second attempt)
                    self.send_dm(
                        user['fields']['Twitter Handle'], 0, user)
                    sleep(5)


def main():
    base_id = "appI43QnVsnxN3yYQ"
    table_name = "Twitch Top 400- Ranked & Scored"
    num_of_attempts = 4
    bot = TwitterBot(base_id, table_name, num_of_attempts)
    bot.run()


if __name__ == "__main__":
    main()
