---
id: "ARCH-ADR-006"
status: "accepted"
decision_scope: "frontend-architecture"
fixed_reference: "docs/architecture/fixed-20260723/impl-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-006. STOMP 연결 소유권과 Snapshot 동기화

## Context

BE는 session/CSRF STOMP, public/private channel, sequence/stateVersion과 snapshot resync를 요구한다. route render와 연결 lifecycle을 분리해야 한다.

## Decision

session-scope connection manager 하나와 feature adapter를 사용한다. native WebSocket을 우선하며 snapshot을 권위로 삼고 version gap·reconnect 시 resync한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| single manager + feature adapter | 연결 안정성과 격리 | lifecycle 규칙 필요 | session auth와 다중 feature에 적합 | 선택 |
| route별 connection | 직관적 | 중복 연결·구독·reconnect 경쟁 | 실시간 경기 route에 위험 | 제외 |
| global STOMP store | 한 곳에서 조회 | channel/feature 강결합 | public/private 경계 약화 | 제외 |
| Query cache 직접 반영 | REST 목록 연동 편리 | ordered game state 주 저장소에 부적합 | 보조 invalidation에만 사용 가능 | 제외 |

## Consequences

connection, subscription과 state reducer를 각각 test한다. BE가 SockJS만 제공하거나 multi-tab/session 정책이 달라지면 transport/lifecycle을 재검토한다.
