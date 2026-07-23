---
id: "ARCH-ADR-018"
status: "accepted"
decision_scope: "ci-cd"
fixed_reference: "docs/architecture/fixed-20260723/harness-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-018. 불변 Artifact 환경 승격

## Context

stage 검증 결과가 production과 동일하려면 environment별 rebuild를 피하고 release 승인과 rollback을 artifact 단위로 해야 한다.

## Decision

PR required check 후 main commit artifact를 한 번 생성하고 stage 자동 배포·smoke 뒤 같은 checksum을 production 승인으로 승격한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| stage auto/prod approval | 검증과 통제 균형 | environment/artifact 관리 | MVP release에 적합 | 선택 |
| main→prod auto | 빠름 | 중단·stage 검증 없음 | session/STOMP 통합 위험 | 제외 |
| 전 환경 manual | 통제 강함 | feedback 늦고 누락 가능 | stage 자동 smoke 이점 포기 | 제외 |
| 환경별 rebuild | 직관적 | 검증 artifact 불일치 | 재현성 위반 | 제외 |

## Consequences

artifact checksum, retention과 deploy adapter가 필요하다. rollback은 이전 artifact 재배포로 한다. 조직이 완전 자동 production 승격을 요구하면 risk와 approval 대안을 재검토한다.
