import pymysql
import os
import json


def lambda_handler(event, context):

    try:
        endpoint = os.environ['RDS_PROXY_ENDPOINT']
        username = os.environ['DB_USERNAME']
        password = os.environ['DB_PASSWORD']
        db_port = int(os.environ['DB_PORT'])

        connect = pymysql.connect(
            host=endpoint,
            user=username,
            password=password,
            database=event.get('db'),
            port=db_port,
            connect_timeout=5,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connect.cursor() as cursor:
            cursor.execute(event.get('query'))
            result = cursor.fetchall()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Success',
                'data': result
            }, default=str)  # datetime 등 객체를 문자열로 변환
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Database query failed: {str(e)}'})
        }