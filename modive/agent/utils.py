import boto3
import os
region_name=os.environ.get('AWS_REGION')
aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')

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
agent_alias_id = os.environ.get('AGENT_ALIAS_ID')
session_id = os.environ.get('SESSION_ID')

def invoke_agent(prompt):
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
