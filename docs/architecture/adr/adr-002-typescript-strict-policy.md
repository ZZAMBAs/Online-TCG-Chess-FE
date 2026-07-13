---
id: "ARCH-ADR-002"
status: "accepted"
decision_scope: "harness"
fixed_reference: "docs/architecture/fixed-20260713/impl-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-002. 강화 TypeScript strict 정책

## Context

REST/STOMP 계약, optional field, 배열 조회와 state version을 안전하게 다뤄야 한다. 초기 구현이 없어 예외 없는 기준을 세울 수 있다.

## Decision

`strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `useUnknownInCatchVariables`를 적용하고 generated type도 검사한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| 강화 strict | 계약·undefined 오류 조기 발견 | 초기 type 작성 증가 | server authority state에 적합 | 선택 |
| 기본 strict만 | 도입이 쉬움 | index/optional 차이를 덜 검출 | 실시간 상태 오류 위험을 충분히 줄이지 못함 | 제외 |
| 디렉터리별 완화 | 빠른 prototype | 예외 누적과 신뢰도 분리 | greenfield에서 필요 근거 없음 | 제외 |

## Consequences

초기 구현 비용을 수용하고 compile-time 안전성을 높인다. generator가 옵션과 호환되지 않으면 generated 전체 제외 대신 generator/adapter를 재검토한다.
