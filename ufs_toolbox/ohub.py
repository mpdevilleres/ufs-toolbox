import os
import tempfile

import requests
import boto3
from urllib.parse import urlparse


class Ohub(object):
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    resource = os.environ.get('RESOURCE')
    auth_url = os.environ.get('AUTH_URL')
    ohub_url = os.environ.get('OHUB_URL')

    def __init__(self, filename=None):
        if filename is None:
            raise ValueError('filename is required')
        self.filename = filename

    def get_access_token(self):
        """
        get access token for ohub API
        :return: access_token, response
        """
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'resource': self.resource
        }
        res = requests.post(self.auth_url, data=payload)
        data = res.json()
        if res.status_code == 200:
            return data['access_token'], res

        return False, res

    def create_header_auth(self):
        access_token, response = self.get_access_token()

        if not access_token:
            raise ValueError('Failed to get access token: ' + response['message'])

        return {'Authorization': 'Bearer ' + access_token}

    def _upload(self, filename=None):
        if filename is None:
            raise ValueError('filename is required')

        header = self.create_header_auth()
        files = {'file': open(filename, 'rb')}
        res = requests.post(self.ohub_url + '/uploadFile', files=files, headers=header)
        if res.status_code == 200:
            return True, res

        return False, res

    def upload(self):
        url = urlparse(self.filename)

        if url.scheme == 's3':
            s3 = boto3.resource('s3')
            fn = url.path.split('/')[-1]
            with tempfile.TemporaryDirectory() as tmpdirname:
                tmp_fn = os.path.join(tmpdirname, fn)
                s3.Object(url.netloc, url.path[1:]).download_file(tmp_fn)
                return self._upload(tmp_fn)
        else:
            return self._upload(self.filename)

    def get_error(self):
        header = self.create_header_auth()
        fn = os.path.split(self.filename)[-1]
        params = {'fileName': fn}
        res = requests.get(self.ohub_url + '/getfileuploaderrorslist', params=params, headers=header)
        if res.status_code == 200:
            return True, res

        return False, res


if __name__ == '__main__':
    ohub = Ohub('s3://ufs-notebooks/Production/data_query/ohub_final/UFS_ARMSTRONG_ORDERSS_20181107065009.csv')
    print(ohub.upload())
