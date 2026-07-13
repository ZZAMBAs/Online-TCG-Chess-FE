# FE Infrastructure Fixed

## 상태와 원천

- status: fixed
- fixed_date: 20260713
- 상세 근거: `docs/architecture/frontend-infrastructure.md`, `docs/architecture/deployment-view.md`
- 관련 ADR: `ARCH-ADR-010`, `ARCH-ADR-011`, `ARCH-ADR-018`

## Deployment Topology

- Vite static SPA artifact를 same-site HTTPS entry에서 제공한다. (`ARCH-ADR-010`)
- HTTPS entry가 static/history fallback, REST proxy, WebSocket upgrade와 security header를 소유한다.
- API/WebSocket 실제 path와 hosting 제품은 미확정이며 fixed 계약 전 추정하지 않는다.
- API와 WebSocket response는 CDN cache 대상이 아니다.

## Artifact와 Environment

- main commit에서 artifact를 한 번 build하고 환경별 rebuild 없이 승격한다. (`ARCH-ADR-011`, `ARCH-ADR-018`)
- 공개 환경 차이는 same-origin runtime public config로 주입한다.
- bootstrap이 config schema를 검증하고 secret/public key allowlist를 적용한다.
- 후보 환경은 local/dev/stage/prod이며 실제 목록은 운영 계획에서 확정한다.

## Cache와 Asset

- content-hashed asset은 immutable cache를 사용한다.
- `index.html`과 runtime config는 짧은 cache 또는 no-store/revalidation을 사용한다.
- font는 승인된 WOFF2를 필요한 weight만 self-host한다.

## Security Headers

- HTTPS entry가 header를 단일 소유한다.
- CSP는 stage report-only 검증 뒤 production enforce한다.
- wildcard, `unsafe-eval`, 임의 inline script를 허용하지 않는다.
- framing 요구가 없으면 `frame-ancestors 'none'`을 적용한다.
- nosniff, referrer와 제한적 permissions policy를 적용한다.
- HSTS와 OAuth에 영향을 줄 수 있는 추가 isolation header는 실제 domain/origin 검증 뒤 적용한다.

## Observability와 Sourcemap

- feature는 vendor-neutral observability adapter만 사용한다.
- release/environment/route/page id와 비민감 오류 분류를 기록한다.
- cookie, CSRF, 사용자 원문과 비공개 game/card 정보를 수집하지 않는다.
- production sourcemap은 public 배포하지 않고 선택 provider에 private upload한다.

## Capacity와 Cost

- 상시 Node SSR/FE application server를 두지 않는다.
- route lazy loading, hashed cache와 정적 hosting을 우선한다.
- bundle, asset, Web Vitals와 artifact 비용은 foundation baseline 뒤 gate로 강화한다.
- preview는 검토가 필요한 PR에만 생성한다.

## 미확정과 전환 조건

- hosting/CDN/reverse proxy 제품
- runtime config key와 실제 환경 목록
- OAuth origin, CSP report endpoint, HSTS 범위
- observability vendor, 보존, alert와 개인정보 근거
- 측정 기반 성능·비용 수치
- SSR/cross-site/multi-CDN 요구가 생기면 관련 ADR을 재검토한다.
