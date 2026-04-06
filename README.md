# streamlit_llm_chat

OpenAI API와 Streamlit을 활용해 만든 **LLM 기반 학습/실무 보조 앱 모음**입니다.  
이 레포지토리는 하나의 단일 앱이 아니라, **자기소개서 첨삭**과 **프로그래밍 학습 챗봇**이라는 두 가지 서브프로젝트를 함께 관리하는 구조로 구성되어 있습니다.

---

## 프로젝트 개요

이 저장소는 프롬프트 설계와 Streamlit UI를 결합해,  
LLM을 실제 사용자가 바로 활용할 수 있는 형태의 웹 애플리케이션으로 구현한 예제 모음입니다.

현재 포함된 프로젝트는 다음 두 가지입니다.

- **resume_feedback**: 직무 기반 자기소개서 첨삭 앱
- **tutor_chatbot**: 역할 전환형 프로그래밍 학습 챗봇

두 프로젝트 모두 다음 공통 구조를 가집니다.

- Streamlit 기반 웹 UI
- OpenAI API 연동
- `.env`를 통한 API 키 관리
- `requirements.txt` 기반 실행 환경 구성

---

## 레포지토리 구조

```bash
streamlit_llm_chat/
├── resume_feedback/
│   ├── .env.example
│   ├── README.md
│   ├── app_resume.py
│   └── requirements.txt
├── tutor_chatbot/
│   ├── .env.example
│   ├── README.md
│   ├── app_chatbot.py
│   └── requirements.txt
└── LICENSE
