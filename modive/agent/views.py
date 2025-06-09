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
        response['answer_type'] = 'chat'

        return Response({'code':status.HTTP_200_OK, 'message':"OK", 'data':response})

class GenerateCustomReport(APIView):
    def post(self, request):

        data = request.data

        agent_response, session_id = invoke_agent_custom_report(data.get('prompt'), data.get('session_id'))

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

class Test(APIView):
    def post(self, request):
        temp = [
            {
                "type": "DailyStatsChart",
                "props": [
                  { "date": '2025-06-01', "userCount": 45, "driveCount": 120 },
                  { "date": '2025-06-02', "userCount": 52, "driveCount": 135 },
                  { "date": '2025-06-03', "userCount": 38, "driveCount": 98 },
                  { "date": '2025-06-04', "userCount": 61, "driveCount": 156 },
                  { "date": '2025-06-05', "userCount": 49, "driveCount": 142 },
                  { "date": '2025-06-06', "userCount": 55, "driveCount": 167 },
                  { "date": '2025-06-07', "userCount": 43, "driveCount": 134 },
                  { "date": '2025-06-08', "userCount": 58, "driveCount": 149 }
                ]
            }
        ]

        response = {
            "answer_type": "dashboard",
            "session_id": "session_id",
            "answer": "completion",
            "components": temp,
        }

        return Response({'code':status.HTTP_200_OK, 'message':"OK", 'data':response})