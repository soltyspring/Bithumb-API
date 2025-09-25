import schedule
import jwt 
import uuid
import hashlib
import time
from urllib.parse import urlencode
import requests
import json
def send_data_to_api(data_dic,accessKey,secretKey):

    apiUrl = 'https://api.bithumb.com'

    
    requestBody = data_dic


    query = urlencode(requestBody).encode()
    hash = hashlib.sha512()
    hash.update(query)
    query_hash = hash.hexdigest()
    #return(requestBody)
    #Generate access token
    payload = {
        'access_key': accessKey,
        'nonce': str(uuid.uuid4()),
        'timestamp': round(time.time() * 1000), 
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secretKey)
    authorization_token = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization_token,
    'Content-Type': 'application/json'
    }

    try:
        # Call API
        response = requests.post(apiUrl + '/v1/orders', data=json.dumps(requestBody), headers=headers)
        # handle to success or fail
        print(response.status_code)
        print(response.json())
        return response.status_code+response.json()
    except Exception as err:
        # handle exception
        return err