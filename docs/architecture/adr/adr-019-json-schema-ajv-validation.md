---
id: "ARCH-ADR-019"
status: "accepted"
decision_scope: "harness"
fixed_reference: "docs/architecture/fixed-20260713/harness-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-019. JSON Schema와 Ajv STOMP 검증

## Context

TypeScript는 실제 STOMP JSON을 검증하지 않는다. BE와 FE가 별도 schema를 유지하면 runtime 검증과 contract fixture가 drift할 수 있다.

## Decision

fixed JSON Schema를 projection하고 Ajv로 주요 inbound/outbound STOMP message를 runtime 검증한다. TypeScript type과 fixture도 같은 원천에서 생성·검증한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| JSON Schema + Ajv | 원천과 runtime 일치 | compile/generation 설정 | BE contract fixture에 적합 | 선택 |
| FE Zod schema | TS/React 사용 편리 | BE schema와 이중 원천 | contract ownership 충돌 | 제외 |
| TypeScript only | build-time 단순 | runtime JSON 미검증 | STOMP state 보호 불가 | 제외 |
| manual guard | dependency 적음 | event 증가 시 누락 | 유지 편차 위험 | 제외 |

## Consequences

invalid message는 store에 적용하지 않고 민감 payload 없이 schema id/path만 관측한다. fixed source가 JSON Schema가 아니면 임의 변환하지 않고 계약 협상 뒤 동등 검증 pipeline을 재검토한다.
