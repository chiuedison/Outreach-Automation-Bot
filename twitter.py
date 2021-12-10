import os
from dotenv import load_dotenv
import tweepy
from pyairtable import Table
from datetime import date, datetime
from time import sleep


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
        self.messages_sent = 0

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
        ''' Checks all the condtions and then sends a direct message to a user '''
        if (user['fields']['Ranking (0 - 4)'] == 0 or user['fields']['Twitter Handle'][0] != '@'):
            return

        attempt_num = user['fields']['Number of attempts']
        # Check if influencer has opted out or expressed interest in GFL
        if (attempt_num > 0):
            try:
                if (user['fields']['Opt-out']):
                    return
            except KeyError:
                pass
            messages = self.twitter_api.get_direct_messages()
            for message in messages:
                if (message._json['message_create']['sender_id'] == user['fields']['recipient_id']):
                    if (message._json['message_create']['message_data']['text'] == 'Opt-out'):
                        self.influencers_table.update(
                            user['id'], {'Opt-out': True})
                        return
                    elif (message._json['message_create']['message_data']['text'] == 'I want to partner'):
                        self.influencers_table.update(
                            user['id'], {'Expressed interest': True})
                        return
            try:
                if (user['fields']['Expressed interest']):
                    return
            except KeyError:
                pass

        if (attempt_num >= self.params['Number of messages']):
            # We already sent the max number of messages
            return
        if (attempt_num > 0):
            # Check the last date we sent a message
            date_today = datetime.today()
            date_last_message = datetime.strptime(
                user['fields']['Last Twitter messages attempt'], "%Y-%m-%d")
            if ((date_today - date_last_message).days < self.params['Frequency of messages (in days)']):
                return

        handle = user['fields']['Twitter Handle']
        # Check if the handle is valid
        try:
            profile = self.twitter_api.get_user(screen_name=handle)
        except tweepy.errors.NotFound:
            self.influencers_table.update(
                user['id'], {'Errors': 'Invalid handle'})
            return

        link = ''
        # Determine if we should add a link to the message
        try:
            self.params['Add link?']
            link = self.params['Link']
        except KeyError:
            pass

        try:
            message = self.params['Message #' + str(attempt_num + 1)]
        except KeyError:
            self.influencers_table.update(
                user['id'], {'Errors': 'Invalid number of messages'})
            return
        # Insert name of the influencer into the message
        if ('!name' in message):
            message = message.replace('!name', user['fields']['Name'])

        reply_options = [
            {
                "label": "Opt-out",
                "description": "Choose this option if you want to stop receiving messages from GFL",
            },
            {
                "label": "I want to partner",
                "description": "Choose this option to speak to a GFL representative",
            },
        ]

        try:
            msg = self.twitter_api.send_direct_message(
                profile.id, message + link, quick_reply_options=reply_options)
            self.influencers_table.update(
                user['id'], {'recipient_id': msg._json['message_create']['target']['recipient_id']})
            self.influencers_table.update(
                user['id'], {'Number of attempts': attempt_num + 1})
            self.influencers_table.update(
                user['id'], {'Twitter DM blocked?': 'No'})
            self.influencers_table.update(user['id'], {'Last Twitter messages attempt': date.today().strftime(
                "%m/%d/%Y")})
            self.messages_sent += 1
        except tweepy.errors.Forbidden:
            self.influencers_table.update(
                user['id'], {'Twitter DM blocked?': 'Yes'})
        self.influencers_table.update(
            user['id'], {'Errors': ''})
        sleep(1)

    def run(self):
        ''' Send messages to streamers on Twiiter '''
        # Get all users from Airtable
        users = self.influencers_table.all()
        for user in users:
            if (user['fields']['Twitter Handle'] == '@pashakhomchenko'):
                self.send_dm(user)
                if (messages_sent >= self.params['Number of messages']):
                    return


bot = TwitterBot()
bot.run()
