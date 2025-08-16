# 자동매매 엔진

이 프로젝트는 이벤트 구동형 자동매매 엔진의 최소 기능 구현(MVP)입니다. 모든 문서는 한국어로 작성되었습니다.

## 구성

- **메시지 계약**: `libs/common/types.py`에 정의된 Pydantic 스키마를 사용합니다.
- **피처/신호**: `features`와 `agents` 모듈에 각종 알파 및 게이트가 구현되어 있습니다.
- **메타 라우터**: `router/meta_router.py`에서 신호를 가중합합니다.
- **리스크/사이징**: `risk` 모듈에서 켈리 비중과 가드레일을 계산합니다.
- **실행**: `exec` 모듈에서 브로커와 실행 엔진을 제공합니다.
- **백테스트**: `sim/backtester.py`는 이벤트 기반 백테스터입니다.

## 체크리스트

- 진입 조건: `edge_hat > gamma*(fee+base_slip)`
- 실패 안전: 데이터 드랍/시계 역행 감지 시 **메이커 온리**
- 로그: 트레이드마다 예상 vs 실현 PnL 분해 1줄 요약
- 대시: Net/Signal/Slip/Fee PnL, Sharpe(롤링), MDD, Turnover, WinRate

## 설치 및 실행

```bash
pip install -e .
pytest
```

더 자세한 내용은 각 모듈의 주석을 참고하십시오.
