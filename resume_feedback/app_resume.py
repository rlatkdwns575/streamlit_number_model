# app_resume.py
import streamlit as st
# OpenAI 클래스를 가져온다
from openai import OpenAI
# .env 파일에서 환경 변수를 로드한다
from dotenv import load_dotenv
# OS 모듈을 가져온다
import os

# .env 파일에서 환경 변수를 로드한다
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
    st.stop()

client = OpenAI()

# ===== 직무별 Few-shot 예시 =====
EXAMPLES = {
    "마케팅": [
        {"role": "user", "content": "자소서: '마케팅에 관심이 있고 열심히 하겠습니다.'\n직무: 마케팅"},
        {"role": "assistant", "content": """**강점**
1. 마케팅 직무에 대한 관심을 표현했습니다.
2. 열정과 의지를 보여주었습니다.
3. 간결한 표현을 사용했습니다.

**개선점**
1. 구체적인 경험이나 성과가 없어 역량 증명이 부족합니다. → 수치가 포함된 경험을 추가하세요.
2. '열심히 하겠습니다'는 모든 지원자가 쓰는 표현으로 차별화가 없습니다. → 구체적 계획으로 대체하세요.
3. 마케팅의 어떤 분야(디지털, 콘텐츠, 브랜딩)에 관심이 있는지 불명확합니다. → 특정 분야를 명시하세요.

**수정된 자소서**
대학 동아리에서 인스타그램 계정을 운영하며 팔로워를 500명에서 3,000명으로 성장시킨 경험이 있습니다.
콘텐츠 기획부터 성과 분석까지 직접 수행하며, 데이터 기반 마케팅의 중요성을 체감했습니다.
이 경험을 바탕으로 귀사의 디지털 마케팅 팀에서 실질적인 성과를 만들어내겠습니다."""},
    ],
    "개발": [
        {"role": "user", "content": "자소서: '코딩을 좋아하고 개발자가 되고 싶습니다.'\n직무: 개발"},
        {"role": "assistant", "content": """**강점**
1. 개발 직무에 대한 열의가 느껴집니다.
2. 직관적이고 솔직한 표현입니다.
3. 핵심 지원 동기가 명확합니다.

**개선점**
1. '코딩을 좋아한다'를 증명할 프로젝트 경험이 없습니다. → GitHub 포트폴리오나 프로젝트 성과를 추가하세요.
2. 어떤 개발 분야(프론트엔드, 백엔드, ML)인지 불명확합니다. → 지원 포지션에 맞는 기술 스택을 명시하세요.
3. 문제를 해결한 구체적 사례가 없습니다. → 디버깅, 성능 개선 등 기술적 문제 해결 경험을 추가하세요.

**수정된 자소서**
학부 캡스톤 프로젝트에서 Python/FastAPI 기반 REST API를 설계하고, 팀원 3명과 협업하여 배포까지 완료했습니다.
응답 속도가 느린 엔드포인트를 캐싱으로 개선하며 평균 응답 시간을 2초에서 0.3초로 단축한 경험이 있습니다.
이 과정에서 체득한 문제 분석-해결 사이클을 귀사의 백엔드 팀에서 발휘하겠습니다."""},
    ],
}


# ======== 첨삭함수 정의 ========
def review_resume(job: str, content: str) -> str:
    system = f"""[Context] 취업 준비생이 {job} 직무에 지원하기 위해 자기소개서를 작성했습니다.
[Objective] 자소서의 강점과 개선점을 분석하고, 합격 가능성을 높이는 수정안을 제시합니다.
[Style] 채용 시장의 최신 트렌드와 직무별 핵심 역량을 기준으로 전문적으로 평가합니다.
[Tone] 격려하되 솔직한 멘토 어조. 강점을 먼저 언급한 뒤 개선점을 제시합니다.
[Audience] 자소서 작성 경험이 적은 대학생 또는 취업 준비생
[Response] 반드시 다음 형식으로 출력하세요:
**강점** (3개, 번호 리스트) → **개선점** (3개, 구체적 이유와 개선 방향 포함) → **수정된 자소서** (완성본, 원문 핵심 메시지 유지)

주의: 지원자가 경험하지 않은 허위 경험이나 성과를 날조하지 마세요."""
    
    few_shot = EXAMPLES.get(job, EXAMPLES["마케팅"])
    messages = [
        {"role": "system", "content": system},
        *few_shot,
        {"role": "user", "content": f"자소서: '{content}'\n직무: {job}"},
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages,
            temperature=0.5,
        )
        return response.choices[0].message.content or "(응답을 생성하지 못했습니다)"
    except Exception as e:
        return f"API 호출 중 오류가 발생했습니다: {e}"
    
# ======== Streamlit 앱 정의 ========
st.set_page_config(page_title="자소서 첨삭 AI", page_icon="📝", layout="centered")
st.title("자소서 첨삭 AI")
st.caption("직무를 선택하고 자소서를 입력하면 맞춤 피드백을 드립니다.")

job_role = st.selectbox("지원 직무", ["Data Scientist", "Software Engineer", "Data Analyst", "Machine Learning Engineer"])
resume_content = st.text_area("자기소개서 입력", height=200, placeholder="첨삭받을 내용을 입력하세요.")

if resume_content:
    st.caption(f"입력 글자 수: {len(resume_content)}")

if st.button("첨삭하기", type="primary", use_container_width=True):
    if not resume_content.strip() or len(resume_content.strip()) < 20:
        st.warning("자기소개서를 최소 20자 이상 입력해주세요.")
    else:
        with st.spinner(f"{job_role}기준으로 첨삭 중... 잠시만 기다려주세요."):
            feedback = review_resume(job_role, resume_content)
        
        st.divider()
        st.subheader(f"첨삭 결과 - {job_role}")
        st.markdown(feedback)

        st.download_button(
            label="첨삭 결과 다운로드",
            data=feedback,
            file_name=f"{job_role}_resume_feedback.txt",
            mime="text/plain",
        )