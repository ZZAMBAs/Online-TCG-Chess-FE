# Frontend Architecture

## 목적

Online TCG Chess MVP의 FE runtime, 상태·통신 경계, module과 component 구조, styling·접근성 기준을 정의한다.

## 원천 산출물

- BE spec commit `a552e06723dc74a427792f10dcfa213540d7e2e4`
- `.cache/prd-read/docs/prd.md`와 기능별 PRD
- `docs/design/design-baseline.md` (`approved`)
- `docs/design/storyboard-manifest.json` (`approved`)
- `docs/architecture/interview-20260713/summary.md`
- 관련 ADR: `ARCH-ADR-001`~`ARCH-ADR-009`, `ARCH-ADR-019`

## 현재 구현 기준 또는 후보 기준

architecture review와 최종 승인을 통과했다. 권위 기준은 `docs/architecture/current-fixed.md`가 가리키는 fixed 문서다. production source와 build 설정은 아직 없어 구현 상태는 fixed architecture의 후속 scaffold 단계다.

## FE 런타임과 빌드 도구

- React + TypeScript + Vite SPA를 사용한다. (`ARCH-ADR-001`)
- route 단위 lazy loading을 기본으로 한다.
- Node SSR server와 edge rendering은 MVP에 포함하지 않는다.
- 정확한 안정 버전은 scaffold 반영 시 공식 지원 관계를 확인해 고정한다.

## TypeScript 정책

- `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `useUnknownInCatchVariables`를 활성화한다. (`ARCH-ADR-002`)
- `@/*` alias는 `src/*`에만 대응한다.
- generated type도 typecheck 대상이며 직접 수정하지 않는다.
- `any`와 무근거 type assertion은 lint와 review 대상이다.

## 라우팅과 라우트 경계

- React Router의 명시적 route config를 사용한다. (`ARCH-ADR-003`)
- 인증, 일반 사용자, 관리자 영역은 layout route로 분리한다.
- root와 영역별 error boundary를 둔다.
- route guard는 화면 접근을 제어하지만 권한의 최종 판정은 서버가 담당한다.
- route metadata에 storyboard page id를 연결한다.

## 상태 관리와 서버 캐시

- form, dialog, 선택 상태는 React local state가 소유한다.
- REST server state는 TanStack Query가 소유한다.
- 경기 snapshot/event와 pending action은 gameplay feature store/reducer가 소유한다.
- route 간 순수 client state가 실제로 생길 때만 Zustand를 도입한다.
- 서버 상태를 Zustand에 복제하지 않는다. (`ARCH-ADR-004`)

## API Client와 오류/Auth 처리

- 모든 REST 요청은 공통 `fetch` transport를 통과한다. (`ARCH-ADR-005`)
- transport는 same-site credential, CSRF header, 전체 요청 timeout/cancel, 공통 오류 mapping을 담당한다.
- TanStack Query cancellation signal과 timeout signal을 결합한다.
- 조회 요청만 제한적으로 retry할 수 있고 변경 요청은 멱등성 근거 없이 자동 retry하지 않는다.
- 세션 만료는 refresh token 흐름이 아니라 session boundary의 로그인 복귀 상태로 처리한다.
- OpenAPI generated client는 feature adapter 뒤에 숨기며 직접 수정하지 않는다.

## BE Contract Collaboration

- REST 권위 원천은 fixed OpenAPI 또는 동등하게 승인된 계약이다.
- STOMP 권위 원천은 fixed schema/fixture다.
- 원천이 없거나 fixed가 아니면 endpoint, payload, destination을 임의 생성하지 않는다.
- breaking change는 BE 확정, FE projection 동기화, generated client·mock 갱신, contract test 순으로 처리한다.

## Generated Client와 Mock 동기화

- OpenAPI client/type은 고정된 생성 명령과 버전으로 만든다.
- CI에서 임시 재생성 결과와 committed output을 비교한다.
- MSW handler는 generated type을 사용하고 누락·obsolete endpoint를 검사한다.
- 생성물과 mock drift는 Hard gate다. (`ARCH-ADR-016`)

## STOMP/WebSocket Client

- `@stomp/stompjs` 기반 session-scope connection manager 하나가 연결을 소유한다. (`ARCH-ADR-006`)
- 우선 native WebSocket을 사용하며 BE 요구 근거가 있을 때만 SockJS를 재검토한다.
- feature는 typed subscription/command adapter만 사용한다.
- route 이탈 시 subscription은 해제하지만 session이 유지되는 동안 connection을 route마다 재생성하지 않는다.
- reconnect는 exponential backoff와 jitter를 사용하되 logout, suspension, authentication failure에는 자동 reconnect하지 않는다.
- snapshot은 최종 권위 상태다. sequence 누락·역전·재접속 시 delta를 추측하지 않고 resync한다.
- action은 `actionId`와 `baseStateVersion`을 포함하고 server event 전까지 pending으로 표시한다.
- fixed JSON Schema가 제공되면 Ajv로 주요 inbound/outbound message를 runtime 검증한다. (`ARCH-ADR-019`)

## 모듈 경계와 import 규칙

```text
app → pages → features → entities → shared
```

- 하위 계층은 상위 계층을 import하지 않는다.
- 서로 다른 feature는 직접 import하지 않는다.
- 재사용 근거가 확인된 코드만 entities 또는 shared로 승격한다.
- dependency-cruiser와 `.mjs` guard로 경계를 강제한다. (`ARCH-ADR-007`)

## 컴포넌트 경계

- page는 route parameter와 여러 feature 조합을 담당한다.
- feature container는 query, store, command를 연결한다.
- entity/shared view는 props와 사용자 event만 처리하고 transport/router를 직접 참조하지 않는다.
- root provider는 router, QueryClient, session, observability로 제한한다.
- feature provider는 route subtree 안에 둔다.
- dialog/sheet focus와 portal은 primitive가, open state와 confirm action은 feature가 소유한다.
- board, card, game HUD는 서버 권위 규칙을 자체 계산하지 않는다.

## 스타일링과 디자인 시스템 경계

- production styling은 CSS Modules와 semantic CSS custom properties를 사용한다. (`ARCH-ADR-008`)
- `shared/styles/tokens.css`가 token import surface다.
- global reset/font/base style은 `shared/styles/index.css`에서 조합한다.
- raw color, spacing, shadow, z-index와 금지 inline style은 style guard로 차단한다.
- runtime 위치·크기는 CSS custom property 전달 방식으로 예외를 제한한다.
- storyboard CSS는 production에서 import하지 않는다.

## 디자인 기준 Source와 승인 상태

- 권위 기준은 `docs/design/design-baseline.md`이며 status는 `approved`다.
- storyboard HTML과 CSS는 검토 자료이고 production dependency가 아니다.
- 실제 production token 값과 primitive 시각 구현은 foundation 이슈가 소유한다.

## 디자이너 협업과 Handoff

- Storybook은 foundation 단계에 token·primitive와 함께 도입한다. (`ARCH-ADR-009`)
- story는 default뿐 아니라 loading, error, empty, disabled, permission, focus, mobile 상태를 포함한다.
- page 전체와 실제 사용자 흐름은 Playwright가 검증한다.

## Breakpoint와 Responsive 기준

- 720px 이하 Mobile, 721px 이상 PC를 기본으로 한다.
- mobile-first로 작성하고 PC에서 정보 병렬성을 확장한다.
- page 전환점은 임의 추가하지 않으며 component 내부는 근거가 있을 때 container query를 사용할 수 있다.

## Accessibility Baseline

- WCAG 2.2 AA를 기준으로 한다.
- semantic HTML, native control, keyboard flow, focus management, non-color state 표현을 강제한다.
- jsx a11y lint와 axe critical/serious 위반은 Hard gate다.
- screen reader 문맥, 읽기 순서, game board 조작은 수동 acceptance로 검증한다.

## Storybook 또는 Component Catalog

- shared UI foundation 이슈에서 Storybook을 설치하고 실제 component story를 작성한다.
- Storybook build는 도입 뒤 Hard gate다.
- representative story가 안정된 뒤 visual regression을 Conditional gate로 승격한다.

## Storyboard-to-Component Traceability

- 정적 구현 manifest가 storyboard page id, route id, page entry를 연결한다.
- Storybook parameter는 관련 component pattern/page id를 기록한다.
- 대표 E2E는 page id와 visual state를 annotation 또는 이름으로 연결한다.
- production runtime은 storyboard manifest를 읽지 않는다.

## Foundation Issue Handoff

- production token과 style entry 구현
- shared primitive와 product surface 구현
- font와 artwork asset 라이선스 확정
- Storybook과 component acceptance 도입
- coverage, bundle, Web Vitals baseline 측정

## 공통 에러/로딩/empty/permission UX

- shared primitive가 표현을 소유하고 feature가 의미와 다음 행동을 mapping한다.
- 예상 API 오류를 route error boundary로 보내지 않는다.
- 인증 만료는 session boundary에서 처리한다.
- reconnect 중 기존 경기 상태를 지우지 않고 연결·resync 상태를 표시한다.
- 상태 UI는 제목, 원인 범주와 가능한 다음 행동을 제공한다.

## 정적 분석과 강제 규칙

- type-aware ESLint, Prettier, import sorting, dependency-cruiser, Stylelint와 `.mjs` guard를 Hard gate로 사용한다.
- Knip은 allowlist가 안정된 뒤 unused export/dependency 차단 gate로 승격한다.

## 테스트와 품질 게이트

- reducer/mapper/schema는 Vitest unit test로 검증한다.
- component는 Testing Library로 사용자 관찰 결과와 a11y role을 검증한다.
- REST adapter는 MSW, STOMP adapter는 fake transport/schema fixture로 검증한다.
- route와 대표 flow는 issue 조건에 따라 Playwright로 검증한다.

## 미확정 사항

- fixed OpenAPI/STOMP 원천 경로와 생성 명령
- API prefix, WebSocket URL/destination, SockJS 필요 여부
- feature별 form library와 상세 client validation
- font/artwork 최종 asset
- route path와 feature별 component 상세 분리
