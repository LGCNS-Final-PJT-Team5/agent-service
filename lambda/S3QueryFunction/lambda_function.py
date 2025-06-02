import boto3
from typing import Dict, Any
from http import HTTPStatus
import time
import json

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        athena = boto3.client('athena')

        action_group = event['actionGroup']
        function = event['function']
        message_version = event.get('messageVersion', 1)
        parameters = event.get('parameters', [])

        query = None
        parameters = event['parameters']
        for parameter in parameters:
            if parameter['name'] == 'query':
                query = parameter['value']

        response = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': 'drive'
            },
            ResultConfiguration={
                'OutputLocation': 's3://modive-kinesis-bucket/2025/'
            }
        )

        execution_id = response['QueryExecutionId']

        # 쿼리 완료 대기
        while True:
            result = athena.get_query_execution(QueryExecutionId=execution_id)
            status = result['QueryExecution']['Status']['State']

            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(1)

        results = athena.get_query_results(QueryExecutionId=execution_id)

        response_body = {
            'TEXT': {
                'body': json.dumps(results['ResultSet']['Rows'])
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