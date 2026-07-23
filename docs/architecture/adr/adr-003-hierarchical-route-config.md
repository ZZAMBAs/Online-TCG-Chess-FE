---
id: "ARCH-ADR-003"
status: "accepted"
decision_scope: "frontend-architecture"
fixed_reference: "docs/architecture/fixed-20260723/impl-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-003. 명시적 계층형 Route Config

## Context

16개 storyboard page, 일반 사용자·관리자·인증 shell과 권한·error boundary를 추적해야 한다.

## Decision

React Router explicit config와 nested layout route를 사용하고 route lazy loading, area error boundary와 storyboard metadata를 둔다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| 계층형 explicit config | 구조·권한·추적이 명확 | 직접 등록 필요 | 승인 page와 shell 분리에 적합 | 선택 |
| file-based routing | 생성 자동화 | plugin과 filename 규칙 의존 | 현재 추가 generator 이점이 작음 | 제외 |
| flat route list | 초기 단순 | guard/layout/error 중복 | 3개 영역과 16개 page에 부적합 | 제외 |

## Consequences

route 추가 시 config와 trace manifest를 함께 수정한다. route 규모가 수동 관리 한계를 넘고 generator 이점이 검증되면 file-based 방식을 재검토한다.
