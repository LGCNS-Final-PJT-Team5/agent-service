from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from agent.utils import invoke_agent_weekly_feedback, invoke_agent_custom_report, create_session, user_type_information

import json

class GenerateWeeklyFeedback(APIView):
    def post(self, request):

        data = request.data
        type_info = user_type_information(data.get('userType'))

        propmt = f'''"userId": "{data.get('userId')}",
        "nickname": "{data.get('nickname')}",
        "userType": "{data.get('userType')}",
        "userTypeDescription": "{type_info.get('summary')}",
        "userTypePersona": "{type_info.get('persona')}",
        "userTypeGoal: {type_info.get('goal')}",
        "scores": "{data.get('scores')}"
        위 정보를 바탕으로 이번 주 주행 리포트 피드백을 생성한다. userType을 잘 반영한 피드백을 생성하는것이 가장 중요하다. userTypeDescription은 타입에 대한 정보, userTypePersona는 에이전트가 피드백을 생성할 때 반영해야하는 정보, userTypeGoal은 이 타입의 사용자가 가야하는 목표다. DynamoDB에서 과거의 주행 데이터를 가져와 비교에 사용한다. JSON 형식 이외에 다른 출력은 하지 않는다.'''

        print(propmt)
        agent_response = invoke_agent_weekly_feedback(propmt)
        print(agent_response)
        response = json.loads(agent_response)

        return Response({'code':status.HTTP_200_OK, 'message':"OK", 'data':response})

class GenerateCustomReport(APIView):
    def post(self, request):

        data = request.data

        prompt = f"""user_prompt: {data.get('prompt')}
        위 내용에 대한 에이전트 응답을 생성한다. 대시보드 생성이 가능하면 대시보드 생성을 우선으로 진행한다. 생성이 불가능할 시 대화를 진행한다. 추가 정보가 필요할 시 사용자에게 질문을 통해 정보를 수집한다. 
        component props를 생성할 때는 지식기반을 참고하여 명확한 구조로 생성한다. 
        component props를 생성할 때 DB에 없는 값 임의 생성하지 않고 DB 조회 결과를 바탕으로 같은 변수명을 사용해 생성한다.
        데이터베이스와 쿼리에 대한 정보가 필요할 시 벡터 데이터베이스를 참고한다.
        닉네임이나 이름을 포함해 입력 시 RDS의 user_db의 users테이블에서 해당 유저의 user_id를 찾아 그 값을 사용한다.
        S3에는 userId로 저장되있으니 userId="RDS에서 가져온 user_id" 로 쿼리를 생성해야한다..
        이모지 문자를 포함하지 않는다.
        JSON 형식 이외에 다른 출력은 하지 않는다.
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
