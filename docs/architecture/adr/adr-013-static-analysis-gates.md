---
id: "ARCH-ADR-013"
status: "accepted"
decision_scope: "harness"
fixed_reference: "docs/architecture/fixed-20260723/harness-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-013. 다층 정적 분석 Gate

## Context

type, format 외에도 import boundary, CSS token bypass와 unused dependency를 자동 강제해야 한다.

## Decision

type-aware ESLint, Prettier/import sort, dependency-cruiser, Stylelint와 custom style guard를 Hard gate로 사용한다. Knip과 warning budget은 baseline 뒤 강화한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| 다층 전용 도구 | 문제별 검출 강함 | config/allowlist 관리 | architecture와 design gate에 적합 | 선택 |
| ESLint 중심 통합 | 도구 적음 | CSS/graph/unused 약함 | 모든 경계를 못 다룸 | 제외 |
| type/lint/format만 | 초기 빠름 | import/token 정책이 문서에 머묾 | 승인 guardrail 부족 | 제외 |
| 전부 즉시 Hard | 엄격 | generated/story false positive | baseline 없는 Knip은 단계화 필요 | 제외 |

## Consequences

tool별 rule owner와 exception fixture를 둔다. 중복 rule이 feedback을 악화시키면 책임을 한 도구로 통합하되 gate 범위는 유지한다.
