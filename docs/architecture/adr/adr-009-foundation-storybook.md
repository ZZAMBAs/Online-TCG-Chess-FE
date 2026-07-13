---
id: "ARCH-ADR-009"
status: "accepted"
decision_scope: "frontend-architecture"
fixed_reference: "docs/architecture/fixed-20260713/impl-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-009. Foundation 단계 Storybook

## Context

approved baseline은 shared primitive, product surface와 상태 variant를 정의한다. 현재 production component는 없다.

## Decision

Storybook 도입을 확정하되 shared UI foundation 이슈에서 token/primitive 구현과 동시에 설치·story 작성한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| foundation Storybook | 실제 component와 catalog 동시 생성 | 설정·story 유지 | 승인 variant handoff에 적합 | 선택 |
| app scaffold 즉시 설치 | 도구 조기 확보 | 표시할 component 없이 재설정 가능 | 현재 source 없음 | 제외 |
| catalog route | app 환경 공유 | production 분리·권한 필요 | 별도 route 비용 | 제외 |
| Playwright only | 실제 flow 강함 | primitive variant 검토 약함 | foundation 검토 surface 필요 | 제외 |

## Consequences

Storybook build를 도입 후 Hard gate로 둔다. page flow는 Storybook에 복제하지 않고 Playwright가 담당한다. catalog 유지 비용이 효용을 넘는 근거가 생기면 범위를 재검토한다.
