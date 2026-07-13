# FE Implementation Architecture Fixed

## 상태와 원천

- status: fixed
- fixed_date: 20260713
- interview: `docs/architecture/interview-20260713/summary.md`
- review: `docs/architecture/interview-20260713/loop-1.md`
- design_source: `docs/design/design-baseline.md` (`approved`)
- 상세 근거: `docs/architecture/frontend-architecture.md`

## Runtime과 Build

- React + TypeScript + Vite SPA를 사용한다. (`ARCH-ADR-001`)
- route lazy loading을 사용하고 Node SSR runtime은 두지 않는다.
- TypeScript 강화 strict와 generated type 검사를 적용한다. (`ARCH-ADR-002`)

## Routing과 Component 경계

- React Router explicit hierarchical config를 사용한다. (`ARCH-ADR-003`)
- 인증·일반 사용자·관리자 layout과 error boundary를 분리한다.
- page는 route와 feature 조합, feature container는 query/store/command 연결, entity/shared view는 props와 event를 담당한다.
- root provider는 router, QueryClient, session, observability로 제한한다.

## State

- local UI state는 React가 소유한다.
- REST server state는 TanStack Query가 소유한다.
- STOMP snapshot/event/pending은 feature store/reducer가 소유한다.
- Zustand는 실제 route 간 client state가 생길 때만 도입하며 server state를 복제하지 않는다. (`ARCH-ADR-004`)

## REST와 Auth

- 공통 `fetch` transport, generated OpenAPI client, feature adapter, TanStack Query 순으로 의존한다. (`ARCH-ADR-005`)
- same-site credential, CSRF, timeout/cancel과 error mapping은 transport가 담당한다.
- 변경 요청은 멱등성 근거 없이 retry하지 않는다.
- session 만료는 login boundary로 처리하고 JWT refresh 흐름을 만들지 않는다.

## STOMP

- session-scope connection manager와 feature subscription/command adapter를 사용한다. (`ARCH-ADR-006`)
- native WebSocket을 우선하며 SockJS는 fixed BE 근거가 있을 때 재검토한다.
- snapshot을 권위로 사용하고 sequence/stateVersion gap·reconnect 시 resync한다.
- 주요 message는 fixed JSON Schema와 Ajv로 runtime 검증한다. (`ARCH-ADR-019`)
- fixed schema가 없으면 destination/payload를 임의 구현하지 않는다.

## Module과 Import

```text
app → pages → features → entities → shared
```

- reverse import와 feature cross import를 금지한다. (`ARCH-ADR-007`)
- 실제 재사용 근거가 생긴 코드만 entities/shared로 승격한다.

## Styling과 Design Handoff

- CSS Modules와 semantic CSS custom properties를 사용한다. (`ARCH-ADR-008`)
- 720px 이하 Mobile, 721px 이상 PC를 기본으로 mobile-first 작성한다.
- storyboard CSS는 production에서 import하지 않는다.
- raw token bypass와 금지 inline style은 guard로 차단한다.
- font는 승인·라이선스 확인된 WOFF2를 self-host하고 확정 전 system fallback을 사용한다.
- 실제 token 값, primitive와 product surface 시각 구현은 foundation TDD가 소유한다.

## Accessibility와 Catalog

- WCAG 2.2 AA를 baseline으로 하고 자동 검사와 수동 acceptance를 병행한다.
- Storybook은 shared UI foundation에서 token/primitive와 함께 도입한다. (`ARCH-ADR-009`)
- page flow는 Playwright가 검증한다.

## Common UX

- shared primitive가 loading/error/empty/permission 표현을 제공한다.
- feature가 오류 의미와 가능한 다음 행동을 mapping한다.
- 예상 API 오류를 route error boundary로 보내지 않는다.
- reconnect 중 기존 game state를 지우지 않는다.

## Traceability

- storyboard page id는 정적 구현 manifest, route metadata, Storybook parameter와 대표 E2E에 연결한다.
- production runtime은 storyboard manifest를 읽지 않는다.

## Hard Constraint와 Handoff

- fixed OpenAPI/STOMP 없이 endpoint, payload, destination을 추정하지 않는다.
- generated code를 직접 수정하지 않는다.
- feature TRD는 이 문서의 runtime, state, transport, import, styling 결정을 재결정하지 않는다.
- 세부 handoff는 `docs/architecture/create-trd-handoff.md`를 따른다.

## 미확정

- fixed OpenAPI/STOMP source path와 generation command
- API/WebSocket path와 SockJS 필요 여부
- feature form 상세와 route path
- font/artwork 최종 asset
