---
id: "ARCH-ADR-016"
status: "accepted"
decision_scope: "harness"
fixed_reference: "docs/architecture/fixed-20260713/harness-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-016. 계약 Drift Gate

## Context

BE spec은 OpenAPI 또는 동등 REST 계약과 검증 가능한 STOMP schema/fixture를 요구한다. hash, generated client, mock 중 하나만 최신이어도 전체 동기화는 보장되지 않는다.

## Decision

fixed source fingerprint, temp regeneration diff, generated client/type, MSW mock, STOMP schema/fixture를 연쇄 검증하고 source가 fixed가 아니면 feature 계약 구현을 차단한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| fingerprint+regen+fixture | 전체 chain 검증 | CI generator 비용 | REST/STOMP 동시 drift에 적합 | 선택 |
| source hash only | 빠름 | generated/mock 상태 모름 | 변경 알림만 가능 | 제외 |
| regeneration only | REST output 강함 | mock/STOMP 별도 누락 | 전체 계약 chain 불충분 | 제외 |
| TypeScript only | 내부 일관성 | BE source drift 감지 불가 | runtime message도 못 검증 | 제외 |

## Consequences

generator determinism과 temp output cleanup이 필요하다. fixed source 형식이 달라지면 동일 보장 수준을 유지하는 대체 pipeline을 재검토한다.
