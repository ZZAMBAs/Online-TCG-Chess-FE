---
id: "ARCH-ADR-008"
status: "accepted"
decision_scope: "frontend-architecture"
fixed_reference: "docs/architecture/fixed-20260723/impl-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-008. CSS Modules와 Semantic Token

## Context

approved design baseline은 semantic CSS token과 token bypass 금지를 정의한다. production styling 기술은 미확정이었다.

## Decision

global semantic CSS custom properties와 component `*.module.css`를 사용하고 raw value/inline style 우회를 guard로 차단한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| CSS Modules + token | runtime 없음, 정적 검사 용이 | variant/class 규칙 필요 | baseline token과 직접 대응 | 선택 |
| Tailwind | 빠른 utility 조합 | token 재투영과 긴 class | 승인 CSS contract 중복 | 제외 |
| Emotion/styled-components | props variant 편리 | runtime·정적 검사 비용 | SSR도 사용하지 않음 | 제외 |
| global BEM | 단순 도구 | 이름·영향 범위 증가 | 16 page에 확장성 낮음 | 제외 |

## Consequences

foundation이 production token과 variant convention을 구현한다. theme runtime switching이나 styling 요구가 크게 달라지면 재검토한다.
