import os
import requests
from dotenv import load_dotenv
from pyairtable import Table


class BearerAuth(requests.auth.AuthBase):
    '''A class for easy authentication with Bearer Token'''

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class Connector:

    def __init__(self):
        '''Currently doesn't initialize any variables'''
        pass

    def getTiltifyData(self):
        '''Currently this method calls Tiltify API and prints out username of authenticated user'''
        url_user = 'https://tiltify.com/api/v3/user'
        auth_class = BearerAuth(os.getenv('TILTIFY_TOKEN'))
        r = requests.get(url_user, auth=auth_class)
        if r.status_code == requests.codes.ok:
            print('Succesful HTTP request to Tiltify API')
        else:
            print('Unsuccesful HTTP request to Tiltify API')
            return
        response_content = r.json()
        print(response_content['data']['username'])

    def updateAirtable(self, base_id, table_name):
        '''Currently this method creates a record in the table, updates it and deletes it'''
        table = Table(os.getenv('AIRTABLE_API_KEY'), base_id, table_name)
        id = table.create({'username': 'edisonc', 'donation': 1000})['id']
        print(table.get(id))
        table.update(id, {'donation': 5000})
        print(table.get(id))
        table.delete(id)


if __name__ == "__main__":
    load_dotenv()
    c = Connector()
    c.getTiltifyData()
    c.updateAirtable(base_id='appySrjTEBJI6l353', table_name='Table 1')
