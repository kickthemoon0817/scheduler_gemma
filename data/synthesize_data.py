import random
import json
from datetime import datetime, timedelta

# Actions
actions = [
    "일정 잡아줘", "예약해줘", "스케줄 해줘", "계획해줘", "등록해줘",
    "일정 추가해줘", "일정 만들어줘", "일정 설정해줘", "일정 예약해줘",
    "일정을 잡아줄래?", "일정 입력해줘", "일정 넣어줘", "일정 정해줘",
    "일정 관리해줘", "일정 생성해줘", "스케줄 추가해줘", "약속 잡아줘",
    "스케줄 등록해줘", "캘린더에 추가해줘", "캘린더에 입력해줘",
    "캘린더에 저장해줘", "일정 기록해줘", "스케줄 작성해줘",
    "일정 기입해줘", "약속 추가해줘", "일정 편성해줘",
    "일정을 예약해줄래?", "새로운 일정 만들어줘", "스케줄을 잡아줘",
    "일정 관리 부탁해", "약속 추가 부탁해", "캘린더 업데이트해줘",
    "일정 세팅해줘", "일정 정리해줘", "일정 등록 부탁해",
    "새로운 약속 잡아줘", "스케줄 설정해줘", "일정을 기입해줄래?",
    "일정 편집해줘", "약속을 추가해줘", "일정을 추가해줄래?",
    "캘린더에 일정 넣어줘", "스케줄을 입력해줘", "일정 스케줄링해줘"
]

# Events
events = [
    "회의", "전화", "약속", "점심 약속", "운동", "과제", "시험", "생일 파티",
    "세미나", "워크숍", "간담회", "출장", "데이트", "모임", "수업", "연습",
    "공부", "미팅",
    "저녁 식사", "아침 식사", "병원 예약", "치과 진료", "영화 관람",
    "콘서트", "공연", "강연", "웨비나", "인터뷰", "직무 교육", "팀 빌딩",
    "연수", "동창회", "기념일", "운동 경기", "축구 경기", "테니스 레슨",
    "요가 수업", "피아노 레슨", "음악회", "미용실 예약", "쇼핑",
    "도서관 방문", "봉사 활동", "공항 픽업", "면접", "사진 촬영",
    "비행기 탑승", "기차 여행", "여행 준비", "회의 준비", "서류 제출",
    "보고서 마감", "회의록 작성", "청소", "이사", "집들이", "요리 교실",
    "언어 교환", "동물병원 방문", "취미 활동", "낚시", "캠핑", "등산",
    "산책", "축제", "예배", "종교 모임", "클럽 활동", "자원봉사",
    "학회 참석", "결혼식", "장례식", "기부 행사", "명절 모임",
    "온라인 회의", "팀 프로젝트", "제품 발표회", "전시회", "박람회",
    "음악 레슨", "미술 수업", "댄스 클래스", "포럼", "이벤트 참석",
    "책 모임", "골프 라운딩", "스키 여행", "해외 출장", "브레인스토밍 세션",
    "제품 출시", "캠페인 기획", "워크숍", "투자 미팅", "고객 상담",
    "계약서 검토", "시연회", "멘토링 세션", "온라인 강의", "연구 발표",
    "아이들 학교 행사", "부모님 방문", "의료 검진", "요리 수업",
    "문화 행사", "시사회", "자격증 시험", "동호회 모임",
    "워크아웃 세션", "비즈니스 런치", "취업 설명회", "네트워킹 이벤트",
    "스포츠 경기 관람", "호텔 예약", "생산 회의", "리더십 교육",
    "보도 자료 발표"
]

# Participants
participants = [
    "김 팀장님과", "개발팀과", "마케팅팀과", "고객님과", "친구들과",
    "가족과", "교수님과", "스터디 그룹과", "팀원들과", "새로운 클라이언트와",
    "운동 동호회와", "동료들과", "상사님과", "동창들과", "파트너와",
    "매니저님과", "디자인팀과", "인사팀과", "재무팀과", "프로젝트 팀과",
    "개발자들과", "마케팅 매니저와", "경영진과", "고객 서비스팀과",
    "영업팀과", "법무팀과", "회계사와", "변호사와", "컨설턴트와",
    "HR 담당자와", "CEO와", "CTO와", "CFO와", "대표님과", "부모님과",
    "형제자매와", "아이들과", "조카들과", "친척들과", "동아리 회원들과",
    "이웃들과", "팀 리더와", "아티스트와", "작가와", "의사와",
    "선생님과", "트레이너와", "코치와", "멘토와", "학생들과",
    "초등학교 친구들과", "고등학교 친구들과", "대학교 동기들과",
    "동기들과", "상담사와", "취미 동호회와", "봉사 단체와",
    "프로젝트 매니저와", "동업자와", "동료 교수들과",
    "팀 매니저와", "프리랜서들과", "파트타임 직원들과",
    "인턴들과", "고문과", "제품 팀과", "QA 팀과", "데이터 분석가와",
    "해외 파트너와", "투자자들과", "비서와", "마케팅 에이전시와",
    "공급업체와", "디스트리뷰터와", "언론사와", "PR 팀과",
    "친구의 가족들과", "동료의 친구들과", "소셜 미디어 팀과",
    "웹 개발자와", "UI/UX 디자이너와", "음악가들과", "사진작가와",
    "영상 제작자와", "리크루터와", "학부모들과", "교직원들과",
    "정부 관계자들과", "NGO 관계자들과", "연구원들과", "애널리스트들과",
    "벤처 캐피탈과", "사업 파트너들과", "이사회와", "상품 기획팀과",
    "국제팀과", "크리에이티브 팀과", "인플루언서와",
    "스타트업 대표들과", "기술 지원팀과", "고객 성공팀과",
    "품질 관리팀과", "물류팀과", "안전 관리팀과", "행사 기획자와",
    "플래너와", "식당 매니저와", "호텔 직원들과"
]

# Times
times = [
    "오늘 오후 2시에", "내일 오전 10시에", "내일 오후 3시에",
    "이번 금요일 오후 3시에", "다음 주 월요일 오전 10시에",
    "오늘 아침 7시에", "오늘 저녁 6시에",
    "이번 주 수요일 오후 1시에", "다음 달 첫째 주 월요일 오전 9시에",
    "이번 토요일 오후 5시에", "내일 저녁 7시에", "오늘 밤 9시에",
    "다음 주 금요일 오후 4시에", "다음 달 15일 오전 11시에",
    "이번 주 목요일 오전 8시에", "모레 오후 2시에",
    "다음 주 화요일 오전 10시에",
    "이번 주말 일요일 오후 3시에", "다음 주 수요일 저녁 6시에",
    "오늘 오후 5시에", "오늘 밤 10시에", "내일 새벽 6시에",
    "다음 주 토요일 오전 11시에", "이번 주 금요일 밤 8시에",
    "다음 달 1일 오후 2시에", "이번 달 말일 오후 3시에",
    "다음 주 목요일 오후 1시에", "이번 주 월요일 오전 7시에",
    "다음 주 수요일 새벽 5시에", "이번 주 토요일 오전 10시에",
    "내일 점심시간에", "오늘 오후 3시 반에", "내일 오후 4시 반에",
    "모레 오전 9시 반에", "다음 주 월요일 오후 2시 반에",
    "다음 주 금요일 오전 11시 반에", "오늘 정오에",
    "이번 주 화요일 오후 1시 15분에", "내일 오전 8시 45분에",
    "다음 주 수요일 오후 5시 30분에",
    "이번 주 일요일 오후 6시 45분에",
    "이번 주 토요일 밤 9시 15분에", "다음 주 화요일 밤 10시에",
    "이번 달 20일 오후 2시에", "내일 오후 1시에",
    "오늘 오전 11시에", "다음 달 둘째 주 목요일 오전 10시에",
    "모레 저녁 7시에", "다음 주 금요일 새벽 5시에",
    "이번 주말 토요일 밤 11시에", "다음 주 수요일 오후 12시에",
    "다음 달 마지막 날 오후 4시에", "내일 오후 6시에",
    "오늘 오후 4시에", "이번 주 목요일 정오에",
    "다음 주 일요일 밤 8시에", "다음 달 5일 오전 7시에",
    "오늘 오후 2시 30분으로", "내일 오전 10시 15분으로",
    "모레 오후 3시 45분으로", "다음 주 수요일 오전 9시 50분으로",
    "이번 주 금요일 오후 4시 20분으로", "오늘 밤 11시로",
    "다음 주 월요일 새벽 6시로", "이번 주 토요일 오전 8시로",
    "다음 달 첫째 주 화요일 오후 5시로"
]

# Modifications
modifications = [
    "시간을 변경할 수 있을까요?", "다른 시간대로 옮길 수 있을까요?",
    "날짜를 바꿔줄 수 있나요?",
    "일정을 수정할 수 있을까요?", "시간을 조정할 수 있나요?",
    "약속 시간을 바꿔주세요.", "시간을 조금 늦출 수 있을까요?",
    "시간을 앞당길 수 있나요?", "다른 날로 변경해줄 수 있나요?",
    "약속을 연기할 수 있을까요?", "일정을 취소하고 다시 잡을 수 있나요?",
    "날짜와 시간을 다시 설정해줄래요?", "일정을 재조정할 수 있나요?",
    "시간을 다시 확인해줄 수 있나요?", "다른 일정으로 바꿔줄 수 있나요?",
    "일정을 변경하고 싶어요.", "날짜를 다시 잡을 수 있나요?",
    "약속을 재설정해줄래요?", "일정을 연기해줄 수 있나요?",
    "시간을 조금 당길 수 있나요?", "날짜를 조금 미룰 수 있을까요?",
    "일정을 취소하고 다른 시간대로 옮길 수 있나요?",
    "약속 시간을 다시 잡아줄래요?", "시간대를 변경해줄 수 있나요?",
    "일정을 변경하고 싶은데 가능할까요?", "다른 날짜로 예약할 수 있나요?",
    "약속 시간을 다시 조정할 수 있을까요?", "일정을 앞당겨줄 수 있나요?",
    "시간을 늦출 수 있을까요?", "다른 날로 연기해줄 수 있나요?",
    "시간 변경이 가능할까요?", "일정을 다시 확인하고 싶어요.",
    "약속 시간을 변경하고 싶습니다.", "다른 시간대를 제안해줄 수 있나요?",
    "일정을 미룰 수 있을까요?", "시간을 조절할 수 있나요?",
    "일정을 다시 계획해줄 수 있나요?", "새로운 시간으로 변경해줄래요?",
    "일정을 다시 잡고 싶습니다.", "약속을 취소하고 싶어요.",
    "시간을 다시 선택하고 싶어요.", "날짜를 변경하고 싶습니다."
]

# New Times
new_times = [
    "오후 3시로", "다음 주로", "다음 날 오전 11시로", "오후 4시로",
    "저녁 7시로", "내일 오후 2시로", "다음 주 월요일 오전 9시로",
    "이번 주 금요일 오후 5시로", "모레 오전 10시로",
    "다음 주 화요일 오후 3시로", "이번 주말로",
    "다음 주 수요일 오후 4시로", "이번 달 말일 오후 2시로",
    "다음 달 첫째 주로", "오늘 저녁 8시로", "내일 오전 11시로",
    "이번 주 목요일 오후 6시로", "다음 주 금요일 오전 10시로",
    "오늘 밤 9시로", "이번 주 토요일 오후 7시로",
    "다음 주 일요일 오전 10시로", "다음 달 15일 오후 3시로",
    "이번 주 수요일 오전 8시로", "다음 주 목요일 저녁 7시로",
    "내일 새벽 6시로", "다음 주 월요일 오전 11시로",
    "모레 오후 2시 반으로", "이번 주 금요일 밤 8시로",
    "다음 주 화요일 밤 10시로", "이번 달 20일 오후 2시로",
    "내일 오후 1시로", "오늘 오전 11시로",
    "다음 달 둘째 주 목요일 오전 10시로",
    "모레 저녁 7시로", "다음 주 금요일 새벽 5시로",
    "이번 주말 토요일 밤 11시로", "다음 주 수요일 오후 12시로",
    "다음 달 마지막 날 오후 4시로", "내일 오후 6시로",
    "오늘 오후 4시로", "이번 주 목요일 정오로",
    "다음 주 일요일 밤 8시로", "다음 달 5일 오전 7시로",
    "오늘 오후 2시 30분으로", "내일 오전 10시 15분으로",
    "모레 오후 3시 45분으로", "다음 주 수요일 오전 9시 50분으로",
    "이번 주 금요일 오후 4시 20분으로", "오늘 밤 11시로",
    "다음 주 월요일 새벽 6시로", "이번 주 토요일 오전 8시로",
    "다음 달 첫째 주 화요일 오후 5시로"
]

# Conflicts
conflicts = [
    "이미 같은 시간에 다른 일정이 있습니다.", "그 시간에는 이미 회의가 잡혀 있습니다.",
    "해당 시간에는 다른 약속이 있습니다.", "그 시간에는 이미 예약이 되어 있습니다.",
    "해당 시간은 이미 차 있습니다.", "그 시간에는 다른 일정이 예정되어 있습니다.",
    "이미 스케줄이 겹칩니다.", "해당 시간은 불가능합니다.",
    "그 시간은 이미 약속이 있습니다.", "동시에 다른 일이 예정되어 있습니다.",
    "그 시간은 이미 바쁩니다.", "해당 시간에는 참여할 수 없습니다.",
    "그 시간에는 이미 선약이 있습니다.", "그 시간에는 다른 미팅이 있습니다.",
    "해당 시간에는 일정이 꽉 차 있습니다.", "그 시간에는 참석이 어렵습니다.",
    "이미 해당 시간에 스케줄이 있습니다.", "그 시간은 이미 일정이 있습니다.",
    "해당 시간에는 다른 업무가 있습니다.", "그 시간에는 일정이 중복됩니다.",
    "해당 시간에는 시간이 없습니다.", "그 시간에는 이미 업무가 예정되어 있습니다.",
    "해당 시간에는 불가합니다.", "그 시간은 이미 예약되었습니다.",
    "이미 해당 시간에 예약이 있습니다.", "그 시간에는 회의가 예정되어 있습니다.",
    "해당 시간에는 약속이 겹칩니다.", "그 시간에는 스케줄이 꽉 찼습니다.",
    "이미 그 시간에는 약속이 있습니다.", "해당 시간에는 일정 조정이 어렵습니다.",
    "그 시간에는 다른 약속이 잡혀 있습니다.", "해당 시간에는 참석 불가능합니다."
]

# Conflict Responses
conflict_responses = [
    "이전에 잡은 일정을 변경하시겠습니까?", "일정을 조정하시겠습니까?",
    "다른 시간대로 변경하시겠습니까?", "새로운 시간으로 재조정할까요?",
    "일정을 다시 잡아드릴까요?", "약속을 변경하시겠습니까?",
    "기존 일정을 취소하시겠습니까?", "다른 날짜로 옮기시겠습니까?",
    "겹치는 일정을 조정할까요?", "다른 시간대로 예약하시겠습니까?",
    "일정을 다시 확인하시겠습니까?", "다른 가능한 시간을 찾아드릴까요?",
    "일정을 재조정하시겠습니까?", "새로운 시간대를 제안드릴까요?",
    "겹치는 약속을 변경하시겠습니까?", "다른 시간대를 선택하시겠습니까?",
    "다른 날로 변경하시겠습니까?", "기존 일정을 변경할까요?",
    "일정을 다시 계획하시겠습니까?", "충돌하는 일정을 조정할까요?",
    "새로운 일정을 잡으시겠습니까?", "겹치는 일정을 취소하시겠습니까?",
    "다른 제안을 드릴까요?", "시간을 다시 선택하시겠습니까?",
    "일정을 연기하시겠습니까?", "일정을 취소하시겠습니까?",
    "다른 날짜를 추천해드릴까요?", "시간을 조정하시겠습니까?",
    "다른 시간으로 변경할까요?", "일정을 변경해드릴까요?",
    "새로운 일정을 계획하시겠습니까?", "시간대를 다시 선택하시겠습니까?"
]

# Reschedule Confirmations
reschedule_confirmations = [
    "알겠습니다. 일정을 변경해 드렸습니다.", "네, 일정을 수정했습니다.",
    "예, 일정을 조정했습니다.", "네, 새로운 시간으로 변경되었습니다.",
    "알겠습니다. 일정을 업데이트했습니다.", "변경 완료했습니다.",
    "네, 일정을 다시 잡았습니다.", "예, 요청하신 대로 일정을 수정했습니다.",
    "네, 일정이 변경되었습니다.", "알겠습니다. 새로운 일정으로 저장했습니다.",
    "예, 일정을 재조정했습니다.", "네, 일정이 업데이트되었습니다.",
    "요청하신 대로 수정되었습니다.", "일정이 성공적으로 변경되었습니다.",
    "네, 일정을 다시 설정했습니다.", "알겠습니다. 일정을 재설정했습니다.",
    "변경 사항을 반영했습니다.", "예, 일정을 연기했습니다.",
    "네, 일정이 연기되었습니다.", "요청하신 대로 일정이 변경되었습니다.",
    "변경이 완료되었습니다.", "네, 새로운 시간으로 일정을 변경했습니다.",
    "일정이 조정되었습니다.", "네, 일정을 수정 완료했습니다.",
    "일정 변경을 완료했습니다.", "네, 새로운 일정으로 업데이트했습니다.",
    "일정을 성공적으로 수정했습니다.", "네, 일정을 다시 예약했습니다.",
    "일정 변경이 완료되었습니다.", "네, 요청에 따라 일정을 수정했습니다.",
    "일정이 변경되어 저장되었습니다.", "네, 일정 조정을 완료했습니다."
]

# Class and Function Definitions
class Conversation:
    def __init__(self, current_date):
        self.messages = [{'role': 'system', 'content': f"오늘은 {current_date}입니다. 한국어로 대답하시오. 당신은 일정을 기록하고, 그것을 관리하는 모델입니다."}]
        self.schedules = []  # List to keep track of scheduled events
    
    def add_message(self, role, content):
        self.messages.append({'role': role, 'content': content})

    def add_schedule(self, participant, event, date, time):
        self.schedules.append({"participant": participant, "event": event, "date": date, "time": time})

    def check_conflict(self, date, time):
        for schedule in self.schedules:
            if schedule["date"] == date and schedule["time"] == time:
                return True, schedule
        return False, None

# Randomize the current date
def random_current_date():
    days_offset = random.randint(-30, 30)  # Random day offset from today, within +/- 30 days
    current_date = datetime.now() + timedelta(days=days_offset)
    return current_date.strftime("%Y년 %m월 %d일")

def random_future_date():
    days_to_add = random.randint(0, 365)  # Random day within the next year
    future_date = datetime.now() + timedelta(days=days_to_add)
    return future_date.strftime("%Y년 %m월 %d일")

def random_future_time():
    hours = random.randint(8, 20)  # Random hour between 8 AM and 8 PM
    minutes = random.choice([0, 15, 30, 45])
    return f"{hours}시 {minutes}분"

def generate_conversation():
    current_date = random_current_date()  # Use the new random date generator
    conversation = Conversation(current_date)
    
    # Step 1: User requests an event to be scheduled
    future_date = random_future_date()
    future_time = random_future_time()
    participant = random.choice(participants)
    event = random.choice(events)
    event_request = f"{participant} {event}를 {future_date} {future_time}에 {random.choice(actions)}."
    conversation.add_message("user", event_request)

    # Check if there's a conflict
    has_conflict, conflicting_event = conversation.check_conflict(future_date, future_time)
    if has_conflict:
        assistant_response = f"그 시간에는 {conflicting_event['participant']}과(와) {conflicting_event['event']}이(가) 예정되어 있습니다. 일정을 조정하시겠습니까?"
        conversation.add_message("assistant", assistant_response)
        
        # User decides to reschedule
        new_future_time = random_future_time()
        modify_request = f"네, 이전 일정을 {new_future_time}로 변경해 주세요."
        conversation.add_message("user", modify_request)
        conversation.add_schedule(participant, event, future_date, new_future_time)
        reschedule_response = f"네, {future_date} {new_future_time}로 {event} 일정을 변경했습니다."
        conversation.add_message("assistant", reschedule_response)
    else:
        # No conflict, add the event
        conversation.add_schedule(participant, event, future_date, future_time)
        assistant_response = f"네, {future_date} {future_time}에 {participant}과(와) {event}을(를) 등록했습니다."
        conversation.add_message("assistant", assistant_response)

    # Step 2: Add more interactions
    for _ in range(random.randint(1, 3)):  # Add between 1 to 3 more interactions
        next_action = random.choice(["add_event", "modify_event"])

        if next_action == "add_event":
            # User adds another event
            new_future_date = random_future_date()
            new_future_time = random_future_time()
            new_participant = random.choice(participants)
            new_event = random.choice(events)
            new_event_request = f"{new_participant} {new_event}를 {new_future_date} {new_future_time}에 {random.choice(actions)}."
            conversation.add_message("user", new_event_request)
            
            # Check for conflict again
            has_conflict, conflicting_event = conversation.check_conflict(new_future_date, new_future_time)
            if has_conflict:
                assistant_response = f"그 시간에는 {conflicting_event['participant']}과(와) {conflicting_event['event']}이(가) 이미 예정되어 있습니다. 일정을 조정하시겠습니까?"
                conversation.add_message("assistant", assistant_response)
                # User decides to cancel or reschedule
                user_decision = random.choice(["cancel", "reschedule"])
                if user_decision == "cancel":
                    cancel_request = "아니요, 다른 시간에 예약하겠습니다."
                    conversation.add_message("user", cancel_request)
                    assistant_response = "네, 해당 일정을 취소했습니다."
                    conversation.add_message("assistant", assistant_response)
                else:
                    new_reschedule_time = random_future_time()
                    reschedule_request = f"네, 이전 일정을 {new_reschedule_time}로 변경해 주세요."
                    conversation.add_message("user", reschedule_request)
                    conversation.add_schedule(new_participant, new_event, new_future_date, new_reschedule_time)
                    reschedule_response = f"네, {new_future_date} {new_reschedule_time}로 일정을 변경했습니다."
                    conversation.add_message("assistant", reschedule_response)
            else:
                conversation.add_schedule(new_participant, new_event, new_future_date, new_future_time)
                assistant_response = f"네, {new_future_date} {new_future_time}에 {new_participant}과(와) {new_event}을(를) 추가했습니다."
                conversation.add_message("assistant", assistant_response)

        elif next_action == "modify_event":
            # User modifies an existing event
            if conversation.schedules:
                event_to_modify = random.choice(conversation.schedules)
                modify_request = f"{event_to_modify['participant']}과(와) {event_to_modify['event']}의 일정을 변경해 주세요."
                conversation.add_message("user", modify_request)
                new_time = random_future_time()

                # Check for conflict before modifying
                has_conflict, conflicting_event = conversation.check_conflict(event_to_modify['date'], new_time)
                if has_conflict:
                    assistant_response = f"그 시간에는 {conflicting_event['participant']}과(와) {conflicting_event['event']}이(가) 이미 예정되어 있습니다. 다른 시간으로 변경하시겠습니까?"
                    conversation.add_message("assistant", assistant_response)
                    user_decision = random.choice(["cancel", "reschedule"])
                    if user_decision == "cancel":
                        cancel_request = "아니요, 다른 시간에 예약하겠습니다."
                        conversation.add_message("user", cancel_request)
                        assistant_response = "네, 해당 일정을 취소했습니다."
                        conversation.add_message("assistant", assistant_response)
                    else:
                        new_reschedule_time = random_future_time()
                        reschedule_request = f"네, {event_to_modify['date']} {new_reschedule_time}로 변경해 주세요."
                        conversation.add_message("user", reschedule_request)
                        conversation.add_schedule(event_to_modify['participant'], event_to_modify['event'], event_to_modify['date'], new_reschedule_time)
                        reschedule_response = f"네, {event_to_modify['date']} {new_reschedule_time}로 일정을 변경했습니다."
                        conversation.add_message("assistant", reschedule_response)
                else:
                    conversation.add_schedule(event_to_modify['participant'], event_to_modify['event'], event_to_modify['date'], new_time)
                    reschedule_response = f"네, {event_to_modify['date']} {new_time}로 일정을 변경했습니다."
                    conversation.add_message("assistant", reschedule_response)
    
    return {"conversation": conversation.messages}

def format_conversation(data_point):
    conversation = data_point["conversation"]
    formatted = "<bos>\n"
    for msg in conversation:
        role = 'assistant' if msg['role'] == 'assistant' else 'user'
        content = msg['content']
        formatted += f"<start_of_turn>{role}\n{content}<end_of_turn>\n"
    formatted += "<eos>\n"
    return formatted

def format_dataset_for_fine_tuning(dataset, output_filename="formatted_korean_scheduling_data.txt"):
    with open(output_filename, "w", encoding="utf-8") as f:
        for data_point in dataset:
            formatted_conversation = format_conversation(data_point)
            f.write(formatted_conversation + "\n")

# Main Execution
if __name__ == "__main__":
    num_conversations = 10000  # Adjust for your dataset size needs
    dataset = [generate_conversation() for _ in range(num_conversations)]
    format_dataset_for_fine_tuning(dataset, "./data/formatted_korean_scheduling_data.txt")
    print("Data generation and formatting complete.")
