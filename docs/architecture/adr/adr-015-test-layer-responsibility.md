---
id: "ARCH-ADR-015"
status: "accepted"
decision_scope: "harness"
fixed_reference: "docs/architecture/fixed-20260723/harness-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-015. 테스트 계층별 책임

## Context

UI behavior, REST cache, ordered STOMP state와 browser flow를 한 test tool로 효율적으로 검증하기 어렵다.

## Decision

Vitest unit, Testing Library component, MSW REST adapter, fake STOMP transport/schema fixture, conditional Playwright E2E/visual smoke로 책임을 분리한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| 계층별 분리 | 빠른 feedback, 실패 원인 명확 | 여러 harness 관리 | REST/STOMP/UI 혼합에 적합 | 선택 |
| Playwright 중심 | 실제 browser 신뢰 | 느리고 세밀한 edge case 어려움 | 모든 contract case에 비효율 | 제외 |
| Vitest/MSW only | 빠름 | route/browser/responsive 누락 | 승인 visual flow 부족 | 제외 |
| 모든 feature E2E | 넓은 flow | 시간·중복·flaky 비용 | issue별 위험 차등 필요 | 제외 |

## Consequences

issue metadata가 E2E/visual 필요성을 결정한다. 경계 중복 test는 줄이고 retry로 flaky를 숨기지 않는다. 실제 위험 분포가 달라지면 gate 비중을 재조정한다.
