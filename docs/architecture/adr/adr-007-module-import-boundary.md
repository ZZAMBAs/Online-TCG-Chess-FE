---
id: "ARCH-ADR-007"
status: "accepted"
decision_scope: "frontend-architecture"
fixed_reference: "docs/architecture/fixed-20260723/impl-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-007. Module과 Import 경계

## Context

storyboard page와 PRD feature를 추적하면서 route composition, 사용자 행동, domain view와 공통 transport를 분리해야 한다.

## Decision

`app → pages → features → entities → shared` 단방향 구조를 사용하고 feature cross import를 금지한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| 계층형 feature 구조 | 의존 방향과 변경 범위 명확 | 경계 판단 필요 | PRD/storyboard trace에 적합 | 선택 |
| route별 folder | page 탐색 쉬움 | domain/action 중복 | 여러 route 공유 기능에 약함 | 제외 |
| 기술별 folder | 초기 단순 | feature 수정 시 전역 folder 이동 | 규모 증가 시 응집도 저하 | 제외 |
| 완전형 FSD | 세밀한 규칙 | segment/public API 비용 | MVP 초기에는 과도 | 제외 |

## Consequences

dependency-cruiser와 guard 설정이 필요하다. 실제 cross-feature orchestration이 반복되면 상위 app/process 계층 추가를 새 ADR로 검토한다.
