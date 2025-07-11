# 트레이딩 봇 웹 애플리케이션 (Trading Bot Web Application)

한국어 요구사항에 따라 구현된 종합적인 트레이딩 봇 웹 애플리케이션입니다.

![Trading Bot Dashboard](https://github.com/user-attachments/assets/f03e8082-825f-4be9-bdd6-6f0ffef8f009)

## 🏗️ 아키텍처 (Architecture)

```
+-------------+      +------------------+
|  ccxt/      |      | yfinance, finnhub |
| 데이터 수집  | ---> | 환율, 주식, 뉴스   |
+-------------+      +------------------+
        |
        v
+------------------+
| pandas, numpy    |
| pandas-ta 지표   |
+------------------+
        |
        v
+---------------------------+
| LangChain / CrewAI Agents |
| - Agent1: 종목비교        |
| - Agent2: 시장심리        |
| - Agent3: 리스크조절      |
| - Agent4: 최종합의        |
+---------------------------+
        |
        v
+-------------------+
| backtrader / ccxt |
| 실전 포지션 관리   |
+-------------------+
        |
        v
+-------------+
| sqlite, csv |
| 로그 기록    |
+-------------+
```

## ✨ 주요 기능 (Features)

### 📊 데이터 수집 (Data Collection)
- **암호화폐 데이터**: CCXT를 통한 Binance 연동
- **주식 데이터**: Yahoo Finance (yfinance)
- **환율 데이터**: Yahoo Finance
- **뉴스 데이터**: Finnhub API

### 📈 기술적 분석 (Technical Analysis)
- **이동평균선**: SMA, EMA
- **모멘텀 지표**: RSI, MACD
- **변동성 지표**: Bollinger Bands, ATR
- **볼륨 분석**: 거래량 패턴 분석
- **자동 신호 생성**: 매수/매도/관망 추천

### 🤖 AI 에이전트 시스템 (AI Agents)
- **Agent 1 - 종목비교**: 상대적 가치 분석 및 종목 간 비교
- **Agent 2 - 시장심리**: 뉴스 감정 분석 및 시장 심리 파악
- **Agent 3 - 리스크조절**: 변동성 분석 및 위험 관리
- **Agent 4 - 최종합의**: 모든 에이전트 의견 종합 및 최종 결정

### 💰 페이퍼 트레이딩 (Paper Trading)
- **가상 포트폴리오**: $100,000 초기 자금
- **실시간 거래 시뮬레이션**: 매수/매도 주문 실행
- **포지션 관리**: 보유 종목 및 수량 추적
- **손익 계산**: 실시간 P&L 및 수익률 계산
- **거래 이력**: 모든 거래 기록 보관

### 🗄️ 로깅 시스템 (Logging System)
- **SQLite 데이터베이스**: 구조화된 데이터 저장
- **시스템 로그**: 모든 활동 기록
- **에이전트 결정**: AI 판단 과정 저장
- **거래 기록**: 포트폴리오 변화 추적

### 🌐 웹 인터페이스 (Web Interface)
- **실시간 대시보드**: 시장 분석 및 AI 추천
- **포트폴리오 관리**: 보유 현황 및 성과 모니터링
- **거래 실행**: 직관적인 매매 인터페이스
- **반응형 디자인**: 모바일 및 데스크톱 지원

## 🚀 설치 및 실행 (Installation & Usage)

### 1. 의존성 설치 (Install Dependencies)
```bash
pip install Flask requests pandas numpy yfinance python-dotenv
# 추가 패키지들 (선택사항)
pip install ccxt finnhub-python pandas-ta
```

### 2. 환경 설정 (Environment Setup)
```bash
cp .env.example .env
# .env 파일에서 API 키 설정
```

### 3. 애플리케이션 실행 (Run Application)
```bash
# 전체 기능 (Flask 필요)
python app.py

# 데모 모드 (의존성 최소화)
python app_simple.py

# 기능 테스트
python demo.py
```

### 4. 웹 인터페이스 접속
브라우저에서 `http://localhost:5000` 접속

## 🎯 사용법 (Usage Guide)

### 시장 분석
1. 대시보드에서 종목 코드 입력 (예: AAPL, BTC/USDT, EURUSD=X)
2. "분석" 버튼 클릭
3. 기술적 지표 및 AI 추천 확인

### 페이퍼 트레이딩
1. 거래 섹션 이동
2. 종목, 매수/매도, 수량, 가격 입력
3. "거래 실행" 버튼 클릭
4. 포트폴리오에서 결과 확인

### 성과 모니터링
- 포트폴리오 섹션에서 현금 잔고 및 손익 확인
- 보유 종목 현황 및 거래 이력 조회
- 로그 섹션에서 시스템 활동 모니터링

## 🔧 기술 스택 (Technology Stack)

### 백엔드 (Backend)
- **Flask**: 웹 프레임워크
- **Python**: 주 개발 언어
- **SQLite**: 데이터베이스
- **pandas/numpy**: 데이터 처리

### 프론트엔드 (Frontend)
- **HTML5/CSS3**: 마크업 및 스타일링
- **Bootstrap 5**: UI 프레임워크
- **JavaScript**: 동적 인터랙션
- **Font Awesome**: 아이콘

### 데이터 소스 (Data Sources)
- **CCXT**: 암호화폐 거래소 API
- **yfinance**: Yahoo Finance 주식 데이터
- **Finnhub**: 뉴스 및 시장 데이터

### AI 및 분석 (AI & Analysis)
- **pandas-ta**: 기술적 분석 라이브러리
- **Custom Agents**: 의사결정 에이전트
- **SQLite**: 데이터 저장 및 로깅

## 🛡️ 안전 기능 (Safety Features)

- **페이퍼 트레이딩 전용**: 실제 자금 위험 없음
- **테스트넷 모드**: 샌드박스 API 사용
- **종합적인 로깅**: 모든 활동 추적
- **위험 관리**: 내장된 리스크 평가
- **에러 처리**: 강건한 예외 처리

## 📁 프로젝트 구조 (Project Structure)

```
bot2/
├── app.py                 # 메인 Flask 애플리케이션
├── app_simple.py          # 간소화된 데모 버전
├── demo.py               # 기능 테스트 스크립트
├── requirements.txt      # Python 의존성
├── .env.example         # 환경 변수 템플릿
├── data_collection/     # 데이터 수집 모듈
│   ├── market_data.py   # 실제 API 연동
│   └── mock_data.py     # 모의 데이터
├── analysis/            # 기술적 분석
│   ├── technical_analysis.py  # 고급 분석
│   └── simple_analysis.py     # 기본 분석
├── agents/              # AI 에이전트
│   ├── agents.py        # 개별 에이전트
│   └── agent_manager.py # 에이전트 관리자
├── trading/             # 거래 시스템
│   └── paper_trader.py  # 페이퍼 트레이딩
├── utils/               # 유틸리티
│   └── database.py      # 데이터베이스 관리
├── templates/           # HTML 템플릿
│   └── index.html       # 메인 대시보드
└── static/              # 정적 파일
    ├── css/style.css    # 스타일시트
    └── js/app.js        # JavaScript
```

## 🚨 면책 조항 (Disclaimer)

이 소프트웨어는 교육 및 시연 목적으로만 제작되었습니다. 실제 거래에 사용하기 전에 충분한 테스트, 위험 관리, 규정 준수가 필요합니다. 거래에는 상당한 금융 위험이 따릅니다.

## 📞 지원 (Support)

문의사항이나 개선 제안이 있으시면 이슈를 등록해 주세요.

---

**구현 완료**: 한국어 요구사항에 따른 완전한 트레이딩 봇 웹 애플리케이션