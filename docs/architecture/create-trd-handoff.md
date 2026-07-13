# Create TRD Handoff

## 목적

기능별 FE TRD가 재결정하면 안 되는 전역 architecture와, 기능별로 구체화해야 할 항목을 구분한다.

## 원천 산출물과 입력 버전

- BE spec commit: `a552e06723dc74a427792f10dcfa213540d7e2e4`
- BE spec sha256: `d0309e904f6c28f2c0f5fb97e4a2d36b0337e262ac85f080fa4de699eae02b4d`
- PRD manifest sha256: `3cc7f1757f7906512fc057c07a81e17ce75721bf8a823675269c070c7d0516de`
- design baseline: `docs/design/design-baseline.md`, approved
- storyboard manifest: version 2, approved, 16 pages
- architecture interview: `docs/architecture/interview-20260713/summary.md`
- fixed architecture: `docs/architecture/current-fixed.md`, `docs/architecture/fixed-20260713`

## 확정된 FE Architecture Constraints

- React + TypeScript + Vite SPA
- explicit hierarchical React Router config
- local/TanStack Query/STOMP feature store/client state 소유권 분리
- common fetch transport와 feature API adapter
- session-scope STOMP manager와 snapshot/version resync
- `app → pages → features → entities → shared` import 방향
- CSS Modules와 semantic token, 720px mobile-first
- page→feature container→entity/shared view component 경계
- WCAG 2.2 AA와 Storybook foundation handoff
- static same-site deployment와 runtime public config

## TRD 필수 준수 Gate

### Hard

- fixed REST/STOMP 계약 없이 endpoint, payload, destination 구현 금지
- generated client 직접 수정 금지
- server authority와 session/CSRF 원칙 준수
- module/import/token boundary 준수
- typecheck/lint/unit/component/adapter/contract/build 통과
- runtime STOMP schema validation과 version gap handling

### Conditional

- issue `e2e_required`에 따른 Playwright
- issue `visual_states`에 따른 desktop/mobile visual smoke
- foundation baseline 이후 coverage/bundle/duration gate

### Advisory

- baseline 전 성능·coverage·unused report
- vendor/hosting 미확정 영역의 후보 비교

## BE 계약 의존성

- REST: fixed OpenAPI source, 생성 command/version, error model, CSRF 전달 방식
- STOMP: handshake URL, destination, public/private channel, JSON Schema/fixture, reconnect/resync
- 공통: errorCode, auth/account/sanction 상태, breaking change procedure
- 현재 fixed contract projection path가 없으므로 계약 확정 전 payload를 추정하지 않는다.

## Storyboard Traceability

| page id | TRD 연결 초점 |
| --- | --- |
| auth-onboarding | session, OAuth, verification, restricted account |
| lobby-quick-match | deck validity, queue lifecycle |
| card-pack-collection | mutation concurrency, daily limit, result |
| deck-builder | local form state, server validation |
| realtime-game | STOMP snapshot/event/pending/resync |
| my-page | account-scoped REST server state |
| match-history | participant authorization, replay data |
| account-info | destructive confirmation, session invalidation |
| settings-notifications | form/mutation/error state |
| blocks-profile-report | permission and moderation action |
| community-list | search/list/empty/permission |
| community-post | editor, ownership, hide/report state |
| admin-report-review | admin route guard, concurrent moderation |
| admin-enforcement | admin form/history/confirmation |
| admin-prohibited-words | validation/table/confirmation |
| admin-card-catalog | read-only admin list/detail |

- 각 TRD는 page id, parent/entry point, desktop/mobile 차이와 representative state를 연결한다.

## 미확정 질문과 소유자

- OpenAPI/STOMP 원천과 경로: BE 계약 협상/`sync-fe-contracts`
- hosting/runtime config/security header 상세: infra/운영
- observability와 개인정보: 운영/security review
- font/artwork license: foundation/design handoff
- exact quality threshold: foundation baseline
- 카드 12장 상세: 상위 요구사항/BE 문서

## 상위 산출물 재검토 필요

- 카드 상세와 fixture가 없는 상태에서 card effect UI/test 값을 임의 확정하지 않는다.
- fixed contract가 storyboard 상태를 지원하지 않으면 계약 또는 storyboard를 재검토한다.
- OAuth/CSRF/STOMP 연결 방식이 BE spec과 다르면 FE architecture를 바꾸지 말고 충돌을 보고한다.

## TRD에서 재결정 금지 항목

- framework/build/runtime
- state ownership 원칙
- REST/STOMP connection·adapter boundary
- module/import direction
- styling/token technology와 breakpoint baseline
- static same-site deployment와 artifact promotion
- test/static/contract/supply-chain gate 분류

## TRD에서 기능별 구체화할 항목

- route path와 route별 data dependency
- form field, client feedback와 server validation mapping
- endpoint/destination 사용과 query key/cache invalidation
- feature state machine과 pending/recovery behavior
- errorCode→사용자 상태/다음 행동 mapping
- component composition과 Storybook 대상
- unit/component/adapter/E2E case와 visual state
