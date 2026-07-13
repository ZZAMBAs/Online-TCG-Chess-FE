---
id: "ARCH-ADR-017"
status: "accepted"
decision_scope: "harness"
fixed_reference: "docs/architecture/fixed-20260713/harness-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-017. Dependency 공급망 Gate

## Context

runtime과 dev dependency 모두 build·release에 영향을 준다. 기존 취약점과 PR에서 새로 도입되는 위험을 구분해 차단해야 한다.

## Decision

lockfile `npm ci`, high/critical audit, 가능한 경우 GitHub dependency review, 단계적 license/signature 검사를 사용하고 자동 force fix/merge를 금지한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| 다층 supply-chain gate | 기존·신규 위험 모두 검출 | exception/policy 관리 | CI release 보호에 적합 | 선택 |
| npm audit only | 단순 | PR diff/license 약함 | 신규 도입 판단 부족 | 제외 |
| dependency review only | PR 신규 위험 강함 | 기존 lockfile 취약점 약함 | 지속 점검 부족 | 제외 |
| bot auto merge | 빠른 update | 검증 전 변화 유입 | release 안전성 저하 | 제외 |

## Consequences

예외에는 만료와 owner가 필요하다. GitHub 기능을 사용할 수 없으면 동일 목적의 대체 scanner를 검토하며 audit false positive 정책도 정기 재검토한다.
