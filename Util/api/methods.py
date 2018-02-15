import requests
from datetime import datetime
from requests.exceptions import HTTPError, RequestException

def get(url, **kwargs):
    start_time = datetime.now()
    raise_error = kwargs.pop('raise', False)
    result = {}

    try:
        response = requests.get(url, **kwargs)
        response.raise_for_status()

        result['success'] = True
        result['error'] = False
        result['response'] = response.json()

        return result
    except HTTPError as error:
        if raise_error:
            raise

        result['success'] = False
        result['error'] = error
        result['response'] = response
        result['status_code'] = response.status_code

    except RequestException as error:
        if raise_error:
            raise

        result['success'] = False
        result['error'] = error
        result['response'] = response

    except ValueError as error:
        if raise_error:
            raise

        result['success'] = False
        result['error'] = error
        result['response'] = response
        result['text'] = response.text

    result['time'] = datetime.now() - start_time
    return result

def post():
    pass