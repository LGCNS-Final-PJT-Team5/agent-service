from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from agent.utils import invoke_agent_weekly_feedback, invoke_agent_custom_report, create_session

import json

class GenerateWeeklyFeedback(APIView):
    def post(self, request):

        data = request.data

        propmt = f'''"userId": "{data.get('userId')}",
        "nickname": "{data.get('nickname')}",
        "userType": "{data.get('userType')}",
        "scores": "{data.get('scores')}"
        위 정보를 바탕으로 이번 주 주행 리포트 피드백을 생성한다. DynamoDB에서 과거의 주행 데이터를 가져와 비교에 사용한다.'''

        agent_response = invoke_agent_weekly_feedback(propmt)
        response = json.loads(agent_response)
        response['answer_type'] = 'chat'

        return Response({'code':status.HTTP_200_OK, 'message':"OK", 'data':response})

class GenerateCustomReport(APIView):
    def post(self, request):

        data = request.data

        prompt = f"""user_prompt: {data.get('prompt')}
        위 내용에 대한 에이전트 응답을 생성한다. 대시보드 생성이 가능하면 대시보드 생성을 우선으로 진행한다. 생성이 불가능할 시 대화를 진행한다.
        component props를 생성할 때는 지식기반을 참고하여 명확한 구조로 생성한다.
        이모지 문자를 포함하지 않는다.
        Json 형식 외에 다른 형식으로 반환하지 않는다. 
        """

        agent_response, session_id = invoke_agent_custom_report(prompt, data.get('session_id'))

        try:
            parse_response = json.loads(agent_response)
            response = parse_response
            response['session_id'] = session_id
        except:
            response = {
                "answer": agent_response,
                "session_id": session_id,
                "answer_type": "chat"
            }

        return Response({'code':status.HTTP_200_OK, 'message':"OK", 'data':response})

class CreateSession(APIView):
    def post(self, request):
        data = request.data

        response = create_session(data.get('userId'))

        return Response({'code':status.HTTP_200_OK, 'message':"OK", 'data':response})
