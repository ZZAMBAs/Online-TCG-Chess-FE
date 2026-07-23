---
id: "ARCH-ADR-001"
status: "accepted"
decision_scope: "frontend-architecture"
fixed_reference: "docs/architecture/fixed-20260723/impl-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-001. React TypeScript Vite SPA

## Context

BE spec은 React same-site client와 REST/STOMP 통신을 전제한다. MVP는 인증 뒤 실시간 경기와 관리 화면 interaction이 중심이고 production FE source와 runtime은 아직 없다.

## Decision

React + TypeScript + Vite SPA를 채택하고 route lazy loading을 사용한다. Node SSR runtime은 운영하지 않는다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| React Vite SPA | 정적 배포, 빠른 개발·build | history fallback과 chunk 관리 필요 | 실시간 인증 앱과 same-site proxy에 적합 | 선택 |
| Next.js SSR/hybrid | SSR, metadata, server 기능 | Node runtime, session/proxy 운영 증가 | 공개 SEO보다 앱 interaction 비중이 큼 | 제외 |
| custom Webpack SPA | 세밀한 build 제어 | 설정·upgrade 비용 | 아직 특수 build 요구가 없음 | 제외 |

## Consequences

정적 artifact와 simple hosting을 얻는 대신 SSR 이점을 포기한다. SEO/SSR 제품 요구가 생기거나 client-only 초기 성능이 측정상 한계가 되면 재검토한다.
