from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from agent.utils import invoke_agent

import json

class TestView(APIView):
    def get(self, request):
        return Response({'status': 'OK'})

class GenerateWeeklyFeedback(APIView):
    def post(self, request):

        data = request.data

        propmt = f'''"userId": "{data.get('userId')}",
        "userType": "{data.get('userType')}",
        "scores": "{data.get('scores')}"
        위 정보를 바탕으로 이번 주 주행 리포트 피드백을 생성한다. DynamoDB에서 과거의 주행 데이터를 가져와 비교에 사용한다.'''

        agent_response = invoke_agent(propmt)
        response = json.loads(agent_response)

        return Response({'code':status.HTTP_200_OK, 'message':"OK", 'data':response})