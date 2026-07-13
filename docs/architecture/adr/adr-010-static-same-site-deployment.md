---
id: "ARCH-ADR-010"
status: "accepted"
decision_scope: "infrastructure"
fixed_reference: "docs/architecture/fixed-20260713/infra-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-010. 정적 SPA와 Same-site Reverse Proxy

## Context

BE spec은 `HttpOnly`, `Secure`, `SameSite=Lax` session cookie와 same-site FE/BE 배포, CSRF와 WebSocket Origin 검증을 요구한다.

## Decision

Vite static artifact를 same-site HTTPS entry에서 제공하고 REST/WebSocket을 reverse proxy한다. Node SSR server는 두지 않는다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| static + same-site proxy | session 경계와 운영 단순 | fallback/cache/proxy 설정 | BE 확정 제약에 적합 | 선택 |
| cross-site hosting | 독립 배포 | cookie/CSRF/CORS/Origin 복잡 | BE same-site 전제 충돌 | 제외 |
| Node SSR | dynamic rendering | runtime·proxy 비용 | 제품 이점 미확인 | 제외 |
| Spring artifact 포함 | same-site 단순 | FE/BE build 강결합 | 독립 검증·승격 저하 | 제외 |

## Consequences

hosting entry가 WebSocket upgrade와 security header를 지원해야 한다. SEO/SSR 또는 cross-site 제품 요구가 확정되면 인증·배포와 함께 재검토한다.
