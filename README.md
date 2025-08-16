# 자동매매 엔진 (MVP)

이 저장소는 이벤트 기반의 간단한 자동매매 엔진 예제입니다. 모든 문서는 한국어로 작성되었습니다.

## 구성 요소
- `ingest`: 오더북 스냅샷과 딥을 재구성하는 모듈
- `features`: OFI, 마이크로프라이스 등 특성 계산
- `agents`: 신호 생성 에이전트
- `router`: 여러 에이전트 출력을 가중합하는 메타 라우터
- `risk`: 켈리 사이징과 가드레일
- `exec`: 페이퍼 브로커 및 실행 엔진
- `sim`: 간단한 이벤트 기반 백테스터
- `dashboards`: PnL 요약 리포트

## 설치
```bash
poetry install
```

## 테스트 실행
```bash
poetry run pytest
```

## 도커 실행
```bash
docker-compose up --build
```

## 데이터 흐름
1. `ingest` 모듈이 시장 상태(`MarketState`)를 생성
2. `agents`가 `AgentResult`를 산출
3. `router`가 가중합하여 `RouterDecision`을 결정
4. `exec` 엔진이 `OrderIntent`를 브로커로 전송
5. 체결(`TradeFill`)이 발생하면 `PnlBreakdown`으로 기록

## 체크리스트
- 진입 조건: `edge_hat > gamma*(fee+base_slip)`
- 실패 안전: 데이터 이상 시 메이커 온리로 전환 (스텁)
- 로그: 체결마다 예상/실현 PnL 요약 (스텁)
- 대시보드: PnL 분해 값 확인 가능 (스텁)

