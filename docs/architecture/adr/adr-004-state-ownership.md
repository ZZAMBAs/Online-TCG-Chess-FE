---
id: "ARCH-ADR-004"
status: "accepted"
decision_scope: "frontend-architecture"
fixed_reference: "docs/architecture/fixed-20260723/impl-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-004. 상태 소유권 분리

## Context

local UI, REST cache, versioned STOMP game state와 route 간 client state는 갱신 방식과 권위가 다르다.

## Decision

React local state, TanStack Query, feature STOMP store/reducer로 분리하고 Zustand는 실제 global client state가 생길 때만 사용한다. server state를 별도 global store에 복제하지 않는다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| 역할별 분리 | cache/version 책임 명확 | 소유자 판단 필요 | REST와 STOMP 혼합 앱에 적합 | 선택 |
| Zustand 단일 store | 단순 접근 | cache·retry·동기화 직접 구현 | server state 중복 위험 | 제외 |
| Redux Toolkit + RTK Query | 강한 통합·devtools | 전역 구조와 boilerplate | 확인된 client global state보다 비용 큼 | 제외 |
| React state only | 의존성 적음 | cache와 route 공유 중복 | API 규모에 부적합 | 제외 |

## Consequences

개발자는 상태 종류를 분류해야 한다. global client state가 복잡해지면 Zustand 범위 또는 Redux 대안을 별도 ADR로 재검토한다.
