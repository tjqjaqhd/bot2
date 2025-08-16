# 자동매매 엔진 (MVP)

이 프로젝트는 이벤트 구동형 자동매매 엔진의 최소 구현 예시입니다. 
Redis, DuckDB 등은 실제 운용 시 필요하나, 본 MVP에서는 단순화를 위해 더미 구성만 포함합니다.

## 설치

```bash
poetry install
```

## 테스트 실행

```bash
poetry run pytest
```

## 구조

```
configs/            설정 파일
libs/common/        공통 타입 및 유틸
features/           OFI, 마이크로프라이스 등 피처
agents/             신호 에이전트
router/             메타 라우터
risk/               사이징 및 가드레일
exec/               브로커 및 실행 엔진
sim/                백테스터(더미)
dashboards/        PnL 리포트(더미)
```

## 체크리스트
* 진입 조건: `edge_hat > gamma*(fee+base_slip)`
* 실패 안전: 데이터 이상 시 메이커 온리 강제
* 로그: 트레이드마다 예상 vs 실현 PnL 분해 출력 (MVP에서는 생략)
* 대시: Net/Signal/Slip/Fee PnL 등 (MVP에서는 간략화)

## 실행 스크립트

`scripts/run_paper.sh`
```bash
#!/bin/bash
echo "페이퍼 모드 시작 (더미)"
```

`scripts/run_live.sh`
```bash
#!/bin/bash
echo "라이브 모드 시작 (더미)"
```
