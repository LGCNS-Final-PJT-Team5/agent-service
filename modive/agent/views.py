from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from agent.utils import invoke_agent_weekly_feedback, invoke_agent_custom_report, create_session

import json

class GenerateWeeklyFeedback(APIView):
    def post(self, request):

        data = request.data

        propmt = f'''"userId": "{data.get('userId')}",
        "userType": "{data.get('userType')}",
        "scores": "{data.get('scores')}"
        위 정보를 바탕으로 이번 주 주행 리포트 피드백을 생성한다. DynamoDB에서 과거의 주행 데이터를 가져와 비교에 사용한다.'''

        agent_response = invoke_agent_weekly_feedback(propmt)
        response = json.loads(agent_response)

        return Response({'code':status.HTTP_200_OK, 'message':"OK", 'data':response})

class GenerateCustomReport(APIView):
    def post(self, request):

        data = request.data

        agent_response = invoke_agent_custom_report(data.get('prompt'), data.get('sessionId'))

        return Response({'code':status.HTTP_200_OK, 'message':"OK", 'data':agent_response})

class CreateSession(APIView):
    def post(self, request):
        data = request.data

        response = create_session(data.get('userId'))

        return Response({'code':status.HTTP_200_OK, 'message':"OK", 'data':response})