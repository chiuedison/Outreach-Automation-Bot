import requests


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

    def getTiltifyData(self, token):
        '''Currently this method calls Tiltify API and prints out username of authenticated user'''
        url_user = 'https://tiltify.com/api/v3/user'
        r = requests.get(url_user, auth=BearerAuth(token))
        if r.status_code == requests.codes.ok:
            print('Succesful HTTP request to Tiltify API')
        else:
            print('Unsuccesful HTTP request to Tiltify API')
            return
        response_content = r.json()
        print(response_content['data']['username'])


if __name__ == "__main__":
    tiltify_token = 'c057949a35b983ff9c4ff4b79bd5a66dad04bb762825ef8533bca7f25ce1efcd'
    c = Connector()
    c.getTiltifyData(tiltify_token)
