import json
from typing import Dict, Any
from http import HTTPStatus
import urllib.request
import urllib.parse


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:

    action_group = event['actionGroup']
    function = event['function']
    message_version = event.get('messageVersion', 1)

    db = None
    query = None

    parameters = event['parameters']
    for parameter in parameters:
        if parameter['name'] == 'db':
            db = parameter['value']
        elif parameter['name'] == 'query':
            query = parameter['value']

    api_url = "https://z1n9fziae8.execute-api.ap-northeast-2.amazonaws.com/prod/lambda-proxy"

    data = {
        "db": db,
        "query": query,
    }

    data = json.dumps(data).encode('utf-8')

    headers = {
        'Content-Type': 'application/json',
    }

    req = urllib.request.Request(api_url, data=data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            j = json.loads(response_data)
            body = json.loads(j["body"])

            response_body = {
                'TEXT': {
                    'body': json.dumps(body['data'])
                }
            }
            action_response = {
                'actionGroup': action_group,
                'function': function,
                'functionResponse': {
                    'responseBody': response_body
                }
            }
            response = {
                'response': action_response,
                'messageVersion': message_version
            }

            return response

    except KeyError as e:
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': f'Error: {str(e)}'
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': 'Internal server error'
        }