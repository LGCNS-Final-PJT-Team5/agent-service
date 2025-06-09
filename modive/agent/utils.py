import boto3
import os

region_name=os.environ.get('AWS_REGION')
aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
agent_kms_arn=os.environ.get('AGENT_KMS_ARN')

bedrock = boto3.client('bedrock',
                       region_name=region_name,
                       aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key
                       )
bedrock_agent = boto3.client('bedrock-agent',
                             region_name=region_name,
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key
                             )
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime',
                                     region_name=region_name,
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key
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