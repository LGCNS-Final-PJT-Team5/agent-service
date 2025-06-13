import boto3
from botocore.config import Config
import os
import json

from botocore.exceptions import EventStreamError

config = Config(
    read_timeout=900,        # 15분 (응답 읽기 최대 시간)
    connect_timeout=60,      # 1분 (연결 시도 최대 시간)
    retries={
        'max_attempts': 5,   # 최대 재시도 횟수
        'mode': 'adaptive'   # 적응형 재시도 (표준, 적응형, 레거시)
    },
    max_pool_connections=50  # 연결 풀 크기
)

region_name=os.environ.get('AWS_REGION')
aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
agent_kms_arn=os.environ.get('AGENT_KMS_ARN')

bedrock = boto3.client('bedrock',
                       region_name=region_name,
                       aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key,
                       config=config
                       )
bedrock_agent = boto3.client('bedrock-agent',
                             region_name=region_name,
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key,
                             config=config
                             )
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime',
                                     region_name=region_name,
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key,
                                     config=config
                                     )

agent = os.environ.get('AGENT')
agent_id = os.environ.get('AGENT_ID')
agent_alias_id = os.environ.get('AGENT_ALIAS')

def invoke_agent_weekly_feedback(prompt):
    session_id = os.environ.get("SESSION_ID")#create_session("weekly_feedback_session")

    res = bedrock_agent_runtime.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        inputText=prompt
    )
    completion=""
    for event in res.get("completion"):
        chunk = event["chunk"]
        completion += chunk["bytes"].decode()

    return completion

def create_session(userId):
    res = bedrock_agent_runtime.create_session(
        encryptionKeyArn=agent_kms_arn,
        sessionMetadata={
            'userId': userId
        },
        tags={
            'userId': userId
        }
    )
    return res['sessionId']

custom_agent = os.environ.get('CUSTOM_AGENT')
custom_agent_id = os.environ.get('CUSTOM_AGENT_ID')
custom_agent_alias_id = os.environ.get('CUSTOM_AGENT_ALIAS')

def invoke_agent_custom_report(prompt, session_id=None):
    try:
        if not session_id:
            session_id = create_session("custom_report_session")

        res = bedrock_agent_runtime.invoke_agent(
            agentId=custom_agent_id,
            agentAliasId=custom_agent_alias_id,
            sessionId=session_id,
            inputText=prompt
        )
        completion = ""
        for event in res.get("completion"):
            chunk = event["chunk"]
            completion += chunk["bytes"].decode()

        return completion, session_id

    except EventStreamError as e:
        print(f"에러 세부사항: {e}")
        print(f"에러 코드: {e.response.get('Error', {}).get('Code')}")
        print(f"에러 메시지: {e.response.get('Error', {}).get('Message')}")
        return "Agent 호출에 실패했습니다. 다시 시도해주세요.", session_id

def user_type_information(type):
    path = os.path.join("agent/type", type) + ".json"
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data