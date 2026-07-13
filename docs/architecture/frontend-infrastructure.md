# Frontend Infrastructure

## 목적

정적 FE artifact, same-site 인증 경계, 환경 설정, 보안 header와 관측·비용 guardrail을 정의한다.

## 원천 산출물

- BE spec commit `a552e06723dc74a427792f10dcfa213540d7e2e4`
- `docs/design/design-baseline.md`
- `docs/architecture/interview-20260713/summary.md`
- 관련 ADR: `ARCH-ADR-010`, `ARCH-ADR-011`, `ARCH-ADR-018`

## MVP FE 인프라 전제

- React Vite SPA를 정적 artifact로 배포한다.
- BE는 server session cookie와 CSRF를 사용하며 FE와 BE는 같은 사이트로 배포한다.
- MVP는 별도 Node SSR server를 요구하지 않는다.

## 배포 형태

- Vite `dist`를 정적 hosting한다. (`ARCH-ADR-010`)
- history route는 `index.html` fallback을 적용한다.
- environment별 rebuild 없이 동일 checksum artifact를 승격한다.

## FE/BE 배포 관계

```text
Same-site HTTPS entry
├─ /, /assets/*         → FE static artifact
├─ /api/*               → BE REST (경로 미확정)
└─ /ws 또는 fixed path  → BE STOMP WebSocket (경로 미확정)
```

- API와 WebSocket의 실제 prefix는 fixed 계약 전까지 확정하지 않는다.
- cross-site CORS와 JWT를 MVP 기본 구조로 사용하지 않는다.

## CDN, Reverse Proxy, Edge

- reverse proxy/hosting이 static route, API, WebSocket upgrade와 security header를 소유한다.
- CDN은 hashed static asset에 선택적으로 사용할 수 있다.
- API와 WebSocket response를 CDN cache하지 않는다.
- hosting/CDN/reverse proxy 제품은 운영 환경 확정 뒤 선택한다.

## 정적 자산과 캐시 정책

- content-hashed asset은 장기 immutable cache를 적용한다.
- `index.html`과 runtime config는 짧은 cache 또는 revalidation/no-store를 적용한다.
- font는 승인·라이선스 확인된 WOFF2만 self-host하며 필요한 weight만 제공한다.
- font asset 확정 전에는 system fallback을 사용한다.

## Environment Strategy

- 동일 artifact를 논리 환경으로 승격한다. (`ARCH-ADR-011`)
- 현재 후보는 local, dev, stage, prod이며 실제 환경 목록은 운영 결정 전까지 미확정이다.
- PR preview는 UI/E2E 검토가 필요한 경우에만 만든다.

## Runtime Config와 공개 변수

- `/runtime-config.json` 같은 same-origin public file을 deploy 시 주입한다.
- app bootstrap에서 schema를 검증하고 필수값이 없으면 configuration error를 표시한다.
- API와 WebSocket은 상대 경로를 기본으로 한다.
- `VITE_*` build-time 변수는 build 자체를 바꾸는 최소 공개값으로 제한한다.

## Secret 노출 방지

- FE environment와 runtime config에는 secret, private key, session/CSRF 값, 내부 credential을 넣지 않는다.
- public config key는 allowlist와 `.mjs` guard로 검사한다.
- sourcemap과 observability metadata에 민감정보를 포함하지 않는다.

## Security Headers

- security header는 HTTPS entry가 단일 소유한다.
- CSP는 stage report-only 검증 뒤 production enforce로 승격한다.
- wildcard, `unsafe-eval`, 임의 inline script를 허용하지 않는다.
- framing 요구가 없으면 `frame-ancestors 'none'`을 적용한다.
- `X-Content-Type-Options`, `Referrer-Policy`, 제한적 `Permissions-Policy`를 적용한다.
- HSTS는 인증서와 하위 domain 영향을 확인한 뒤 적용한다.
- OAuth 호환성 검증 전 COOP 같은 추가 격리 header를 임의 적용하지 않는다.

## Client Observability

- `shared/observability` adapter만 feature에 노출한다.
- release commit, environment, route/page id, 오류 분류와 Web Vitals를 구조화한다.
- email, nickname, cookie, CSRF, 채팅·게시글 원문, 비공개 카드 정보는 수집하지 않는다.
- 예상 API/validation 오류를 exception으로 과다 수집하지 않는다.

## Sourcemap와 Release Version

- production sourcemap은 public asset으로 배포하지 않는다.
- 선택한 관측 시스템에 release별 private upload하고 upload 성공과 public 제외를 검증한다.
- vendor 미선정 상태에서도 release tag와 console error hygiene를 유지한다.

## Capacity/Cost Guardrail

- 상시 FE application server와 필수 edge function을 두지 않는다.
- route lazy loading과 hashed asset cache를 사용한다.
- build마다 total/route chunk/font/image 크기를 기록한다.
- foundation baseline 뒤 bundle과 성능 증가 gate를 강화한다.
- preview, observability, CI artifact 비용과 보존 정책을 함께 관리한다.

## MVP 제외 확장 후보

- Node SSR, edge rendering
- image transformation service
- multi-CDN
- cross-site FE/BE 배포
- 측정 근거 없는 별도 FE application server

## 후속 스킬 연계

- 계약 협상/`sync-fe-contracts`: API/WebSocket 경로와 origin
- foundation issue: font/artwork, bundle baseline
- `security-review`: CSP, OAuth, 개인정보와 threat 상세
- 운영 문서: hosting vendor, HSTS, alert와 rollback runbook

## 미확정 사항

- hosting/CDN/reverse proxy 제품
- 환경 목록과 runtime config key
- OAuth origin, CSP report endpoint, HSTS 범위
- observability vendor, 보존·alert·개인정보 기준
- 성능·비용 수치
