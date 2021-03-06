import requests
from django.shortcuts import render

from .models import Question

def create_questionDB():
    common_question_list = [
        '자신의 장점과 단점은 무엇인가요?', 
        '이 대학(학과)에 지원하게 된 동기는 무엇인가요?',
        '어떤 계기로 봉사활동을 하게 됐나요?',
        '어떤 분이 가장 기억에 남나요?', 
        '본인한테 봉사는 어떤 의미인가요?', 
        '이 대학(학과)에 지원하기 위해 어떤 노력을 하였나요?',
        '입학 후 학업계획에 대해 말해보세요.',
        '본인의 삶에 가장 영향을 미치는 사람(책, 사건 등)은 무엇인가요?',
        '대학 졸업 10년 후 본인이 하고 있는 일에 대해 말해 보세요.',
        '학창시절 가장 인상 깊었던 체험이 있다면 이야기 해보세요.',
        '수상을 많이 했고 다양한 대회에 참여했는데 이렇게 많이 참여한 동기는 무엇인가요?',
        '진로가 바뀌게 된 시점에 영향을 준 활동은 무엇인가요?',
        '3년동안 교내 활동을 하면서 기억에 남는 것이 있다면, 과정과 결과를 간단하게 소개 해주세요.',
        '조별 보고서를 작성하면서 본인은 어떤 역할을 수행하였는지 설명해주세요.',
        '친구들이 지원자를 오해하여 가장 속상하였을 때는 언제인가요? 당시 어떻게 대처하였나요?',
        '고등학교 재학 중 좋은 성적을 유지한 자신만의 공부 방법은 무엇인가요?',
        '본인이 이 학과와 잘 맞는다고 생각하는 강점과 그 이유를 설명해보세요.',
        '인생에서 가장 소중하다고 생각하는 것 2~3가지를 말해 보세요',
        '학교 다닐 때  가장 좋아하는 과목과 그 이유는 무엇인가요?',
        '학교생활을 하면서 아쉬운 점을 말해 주세요.',
        '이 학과에서 학생을 뽑아야하는 이유가 있다면 무엇인가요?',
        '자신의 창의성을 발휘한 활동은 무엇인가요?',
        '마지막으로 하고 싶은 말은 무엇인가요?',
        '입학 후의 희망 세부 전공분야를 말하고, 그 분야의 기술현황을 설명하세요']
    computer_question_list = [
        '벡터와 스칼라의 차이는 무엇인가요? 그리고 벡터의 구성요소에 관해 설명하세요.',
        '프로그램을 제작한다고 가정했을 때, 만들어보고 싶은 프로그램은 무엇인가요?',
        '모바일 시대가 열린 지금, PC와 모바일기기의 공통, 차이점은 무엇인가요?',
        '가장 자신있는 컴퓨터 언어가 무엇인가요?',
        '로봇에 관심이 많다고 적었는데, 현재 그 산업의 동향을 알고 있나요?',
        '휴대폰을 이용한 현재 서비스 종류와 미래에 예상되는 서비스를 말해주세요.',
        '전자게시판의 실명제 도입 장/단점을 설명하고 실명제의 필요성에 대한 자신의 견해를 피력하세요.',
        '스팸 메일의 정의와 유해성을 설명하고, 스팸메일 처리 방식에 대해 아는대로 설명해주세요.',
        '홈페이지 제작과정에 대해서 설명해주세요.',
        '게임개발과 관련한 자신의 미래계획이나 포부를 말해보세요.']
        
    business_question_list = [
        '수상경력이 굉장히 많은데 가장 좋아하는 과목을 말하고 이를 경영과 관련시켜서 말해보세요.',
        '생기부에 사회적 이슈들에 굉장히 관심있다고 적혀있는데 최저임금에 대한 기업의 입장의 장단점에 대해 말해보세요.',
        '진로는 홍보전문가이고, 취미는 맛집탐방인데 요새 맛집 마케팅 중에 인상깊은 것 말해볼까요?',
        '독서활동 중에 경영과 관련 책에 대해 이야기해보세요.',
        '회계랑 경영학이 자신한테 맞는다고 생각하시는 이유가 있나요?',
        '동아리에서 전문경영인과 오너경영인에 대해 발표했는데 이 둘의 차이를 설명해줄래요?',
        '자신이 지향하는 사회는 무엇인가요?',
        '요즘 YOLO가 뜨고 있는 트렌드인데 이런 YOLO가치관을 가지고 있는 소비자들을 위한 마케팅에는 무엇이 있을까요?',
        '실버산업이 요즘 대두되고 있습니다. 독거노인 등 경제적으로 어려운 노인들을 실버산업 참여로 이끌기위해 학생은 금융기업 입장에서 어떤 마케팅을 할 것인가요?',
        '기업의 사회적 책임에 대해 이야기해보세요.',
        '4차산업혁명 시대에 발맞추어 경영학과 IT 기술의 융복합 사례로는 어떤 것들이 있나요? 또 그 효과는 무엇인가요?',
        '공유경제 아나요? 예를 들면 자전거를 대여해주는 시스템이요. 그런게 갑자기 요즘 시대에 왜 생겼다고 생각하나요?',
        '한일무역 규제에 대해 어떻게 생각하나요?'
]
    korean_question_list = [
        '본인이 생각하는 정보사회의 장단점에 대해 말씀해주세요',
        '국어국문학과를 입학하게 되면 가장 배우고 싶은 것은 무엇인가요?',
        '독서활동이 많은데, 지금 읽은 것들 중에서 친구들에게 어떤 책을 추천하고 싶은가요?',
        '가장 인상깊게 읽은 책이 무엇인가요?',
        '전공을 정할 때 가장 큰 영향을 준 책 한권에 대해 이야기 해주세요.',
        '좋은 글이란 어떤건가요?',
        '글쓰기 상을 많이 받았는데 가장 기억에 남는 대회는 무엇인가요?',
        '문학과 현실의 관계에 대해 어떻게 생각하나요?',
        '좋아하는 작가는 누구이고, 그 작가의 어떤 작품을 좋아하는지 말씀해주세요.',
        '한국문학의 세계화가 지니는 가치는 무엇인가요?'
    ]
    biology_question_list = [
        '화생공 대신 왜 생명공학부에 지원했는가요?',
        '수학과 생명과학이 관련된 점은 무엇인가요?',
        '단백질의 1,2,3,4차 구조에 대해 설명해주세요.',
        '교감신경과 부교감 신경에 대해 아나요?',
        '본인이 배운 생명이라는 과목 내에서 가장 관심이 많은 내용은 무엇인가요?',
        '바이러스는 생물일까 무생물일까 자신의 생각을 말해보세요.',
        '미생물에는 무엇이 있나요?',
        '생명공학과 관련해서 읽은 책이 있나요?',
        '생명과학과 관련된 비교과 활동은 무엇인가요?',
        '고등학교 생명과학 1,2 내용 중에서 가장 재미있었던 내용은 무엇인가요?'
    ]
    
    for question in common_question_list:
        Question.objects.filter(question=question).delete()
        Question(question=question,department=0).save()
    
    for question in computer_question_list:
        Question.objects.filter(question=question,department=1).delete()
        Question(question=question,department=1).save()

    for question in business_question_list:
        Question.objects.filter(question=question,department=2).delete()
        Question(question=question,department=2).save()

    for question in korean_question_list:
        Question.objects.filter(question=question,department=3).delete()
        Question(question=question,department=3).save()
    
    for question in biology_question_list:
        Question.objects.filter(question=question,department=4).delete()
        Question(question=question,department=4).save()

    
def db(request):
    create_questionDB()
    q_list = Question.objects.order_by('-question')
    return render(request, 'questionDB.html',{'q_list':q_list})
