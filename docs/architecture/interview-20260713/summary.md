# Architecture Interview Summary

## 실행 정보

- 실행 날짜: 2026-07-13
- 상태: architecture review pass, fixed 승인 완료
- 리뷰 루프 횟수: 1
- 최종 fixed 디렉터리: `docs/architecture/fixed-20260713`

## 사용한 원천 문서

- `AGENTS.md`
- BE `master` `docs/spec/spec-fixed.md`
  - commit: `a552e06723dc74a427792f10dcfa213540d7e2e4`
  - sha256: `d0309e904f6c28f2c0f5fb97e4a2d36b0337e262ac85f080fa4de699eae02b4d`
  - verified_at: 2026-07-13, `git-ls-remote`
- `.cache/prd-read/docs/prd.md`
- `.cache/prd-read/docs/features/*/prd.md`
- `.cache/prd-read/docs/traceability.md`
- `docs/design/design-baseline.md` (`approved`)
- `docs/design/storyboard-manifest.json` (`approved`, version 2, 16 pages)
- `docs/design/storyboard-pages.md`
- `package.json`

## 현재 저장소 상태

- production `src`와 FE build/test 설정은 아직 없다.
- `package.json`에는 Husky 준비 script와 dependency만 있다.
- 기존 fixed architecture와 architecture review ledger는 없다.
- 이번 결정은 기존 구현 교체가 아니라 MVP FE 전역 architecture와 harness의 최초 기준 확정이다.

## 질문한 아키텍처 영역과 승인 결정

### FE 구현 아키텍처

- React + TypeScript + Vite SPA를 채택한다.
- TypeScript는 `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `useUnknownInCatchVariables`를 적용한다.
- React Router의 명시적 계층형 route config와 사용자·관리자·인증 layout boundary를 사용한다.
- 상태는 React local state, TanStack Query REST server state, STOMP feature store, 조건부 Zustand client state로 나눈다.
- REST는 공통 `fetch` transport, OpenAPI generated client, feature adapter, TanStack Query 순으로 의존한다.
- STOMP는 세션 단위 connection manager와 feature subscription adapter를 사용하고 snapshot과 `sequence/stateVersion`을 권위 기준으로 삼는다.
- source는 `app → pages → features → entities → shared` 단방향 import 구조로 둔다.
- page는 조합, feature container는 query/store/command 연결, entity/shared view는 props와 사용자 event를 담당한다.
- 공통 loading/error/empty/permission 표현은 shared primitive가, 오류 의미와 다음 행동은 feature가 담당한다.

### 디자인 시스템과 접근성

- production styling은 CSS Modules와 semantic CSS custom properties를 사용한다.
- storyboard CSS를 production에서 직접 import하지 않는다.
- 720px 이하 Mobile, 721px 이상 PC를 기본 전환점으로 사용하고 mobile-first로 작성한다.
- 승인·라이선스 확인된 WOFF2 font를 self-host하고, 확정 전에는 system fallback을 사용한다.
- Storybook은 shared UI foundation 이슈에서 token·primitive 구현과 함께 도입한다.
- WCAG 2.2 AA를 baseline으로 삼고 자동 검사와 수동 acceptance를 병행한다.
- storyboard page id는 정적 manifest, route metadata, Storybook parameter, 대표 E2E annotation으로 추적한다.

### FE 인프라

- Vite `dist`를 정적 hosting하고 같은 사이트 HTTPS 진입점에서 `/api`와 WebSocket 경로를 BE로 proxy한다.
- 동일 artifact를 환경별로 다시 build하지 않고 runtime public config로 승격한다.
- 보안 header는 hosting/reverse proxy가 단일 소유하며 CSP는 report-only 검증 후 enforce한다.
- client observability는 vendor-neutral adapter를 사용하고 production sourcemap은 공개하지 않는다.
- 정적 hosting을 우선하고 bundle, asset, Web Vitals, artifact 비용은 foundation baseline 이후 gate로 승격한다.

### CI/CD와 AI harness

- npm, committed `package-lock.json`, pinned Node/npm policy를 사용한다.
- typecheck, type-aware ESLint, Prettier, import sorting, dependency-cruiser, Stylelint, `.mjs` guard를 Hard gate로 둔다.
- Knip과 warning budget은 baseline과 allowlist 안정화 뒤 Hard/Conditional gate로 승격한다.
- pre-commit은 staged fast check, pre-push는 변경 영향 검사, CI는 전체 검사를 같은 `.mjs` entrypoint로 실행한다.
- Vitest, Testing Library, MSW, STOMP fake transport/fixture, Playwright를 책임별로 분리한다.
- E2E와 visual smoke는 이슈의 `e2e_required`와 `visual_states`에 따라 Conditional gate로 실행한다.
- OpenAPI/STOMP source fingerprint, 임시 재생성 diff, generated client, MSW mock, schema fixture drift를 검사한다.
- STOMP runtime message는 fixed JSON Schema를 Ajv로 검증한다.
- npm audit high/critical, lockfile 재현, 가능한 경우 GitHub dependency review를 차단 gate로 사용한다.
- PR 검증 뒤 main artifact를 한 번 만들고 stage 자동 배포, production 승인 승격을 수행한다.
- required test retry는 기본 0이며 coverage, 실행 시간, bundle budget은 측정 baseline 뒤 강화한다.
- `main`은 보호하고 작업 branch PR과 squash merge를 사용한다.

## 검토한 대안과 채택·제외 이유

각 의미 있는 대안 비교는 인터뷰 당시 `proposed`로 작성했고 최종 승인 후 `accepted`로 전환한 `docs/architecture/adr/`에 보존한다. 공통 제외 경향은 다음과 같다.

- Next.js SSR과 Node FE server는 인증 후 실시간 interaction 중심 MVP에서 운영 비용 대비 이점이 작아 제외했다.
- Redux Toolkit + RTK Query는 가능한 대안이지만 현재 확인된 global client state보다 전역 구조 비용이 커 제외했다.
- Axios는 단계별 transfer timeout이나 progress 요구가 생기면 재검토하되 현재 JSON REST에는 중앙 `fetch` transport로 충분하다고 판단했다.
- Tailwind와 CSS-in-JS는 승인된 semantic token의 직접 적용과 정적 style guard에 CSS Modules가 더 단순해 제외했다.
- 환경별 build는 stage에서 검증한 artifact와 production artifact가 달라지는 위험 때문에 제외했다.
- hook 전체 검사와 CI retry는 느린 feedback 또는 flaky 은폐 위험 때문에 제외했다.

## 생성한 아키텍처 ADR

- `ARCH-ADR-001`부터 `ARCH-ADR-019`까지 생성하고 최종 승인 후 accepted로 전환했다.
- ADR index: `docs/architecture/adr-index.md`
- fixed reference는 구현 9건, 인프라 2건, 하네스 8건의 fixed 문서에 연결했다.

## 미확정 사항

- fixed OpenAPI와 STOMP schema의 실제 원천 경로, 생성 명령, API prefix, WebSocket URL/destination
- SockJS 필요 여부
- hosting/CDN/reverse proxy 제품, 실제 환경 목록과 runtime public config key
- OAuth origin, CSP report endpoint, HSTS `includeSubDomains` 범위
- observability vendor, 보존 기간, alert threshold, 개인정보 처리 근거
- font·체스 기물·카드 artwork의 최종 자산과 라이선스
- 정확한 Node/npm 및 도구 버전
- coverage, bundle, Web Vitals, test duration, artifact retention 수치
- GitHub environment 권한과 required reviewer 수
- MVP 카드 12장 상세 정의와 fixture

## 상위 산출물 재검토와 후속 연계

- 계약 협상과 `sync-fe-contracts`: OpenAPI/STOMP fixed 원천과 FE projection 확정
- `create-trd`: 기능별 route, form, 상태, 오류와 계약 사용 상세화
- foundation issue: token, primitive, product surface, font asset, Storybook 구현
- `create-issues-adr`: feature/foundation 구현 issue와 구현 ADR
- `security-review`: XSS, CSRF, 개인정보, abuse case 상세 검토
- `e2e-test`: 이슈별 desktop/mobile, 오류·권한·실시간 상태 검증

## 리뷰 루프

| loop | 상태 | 보완 문서 | 결과 |
| --- | --- | --- | --- |
| 1 | review-pass | fixed 문서, ledger, ADR 상태·reference, index, traceability | 사용자 승인 후 fixed 완료 |
