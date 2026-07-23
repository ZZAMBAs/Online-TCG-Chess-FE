---
id: "ARCH-ADR-011"
status: "accepted"
decision_scope: "infrastructure"
fixed_reference: "docs/architecture/fixed-20260723/infra-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-011. Runtime Public Config

## Context

stage에서 검증한 artifact와 production artifact가 동일해야 하며 static SPA에는 environment별 공개 설정 차이가 있다.

## Decision

artifact를 한 번 build하고 deploy 시 same-origin runtime public config를 주입한다. bootstrap schema validation과 secret allowlist를 적용한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| runtime config file | 동일 artifact 승격 | bootstrap/schema 필요 | stage-prod 재현성에 적합 | 선택 |
| 환경별 VITE build | Vite 기본 방식 | 환경별 artifact 차이 | 검증 동일성 저하 | 제외 |
| code hardcode | 가장 단순 | preview/stage 대응 약함 | 다중 환경 후보 존재 | 제외 |
| index 치환 | 첫 요청에 주입 | HTML 변환·escaping 필요 | static file보다 운영 복잡 | 제외 |

## Consequences

runtime config cache와 validation error UX가 필요하다. hosting이 atomic config/artifact promotion을 지원하지 않으면 deploy adapter를 재검토한다.
