import boto3
from boto3.dynamodb.conditions import Attr
from typing import Dict, Any
from http import HTTPStatus
import json

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:

        action_group = event['actionGroup']
        function = event['function']
        message_version = event.get('messageVersion', 1)

        userId = None
        parameters = event['parameters']
        for parameter in parameters:
            if parameter['name'] == 'userId':
                userId = parameter['value']

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table("weekly-dashboard")

        response = table.scan(
            FilterExpression=Attr('userId').eq(userId)
        )['Items']

        def get_created_at(item):
            return item.get('createdAt')

        sorted_items = sorted(response, key=get_created_at,  reverse=True)
        recent_5 = sorted_items[:min(5, len(sorted_items))]

        response_body = {
            'TEXT': {
                'body': json.dumps(recent_5)
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
        print(response)
        return response

    except KeyError as e:
        print(e)
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': f'Error: {str(e)}'
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': 'Internal server error'
        }
