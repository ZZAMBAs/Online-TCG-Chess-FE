# Architecture Review Ledger

## 목적

fixed architecture 이후 요구사항·디자인·계약·구현·CI/배포 변경에 따라 재검토할 영역과 안전한 생략 근거를 기록한다.

## 리뷰 기준

- last_reviewed_at: 2026-07-23
- result: `review-pass` (contract reconfirmation)
- skipped_area: 없음. 최초 review이므로 모든 영역을 검토함
- design_baseline_sha256: `49a4875df222fe2c8c49721f38b517d9b3c4cf994b87ba6b97d1f1b0ec092fef`
- storyboard_manifest_sha256: `c00e7a9709786536074a9f40c54da7cac7f483d7316f69227a21fa248e241d97`
- impl_fixed_sha256: `1c4465f7fda7e9f95e831b21b1c6dc50e1fa13a20296f28597e3c1c42844e29d`
- infra_fixed_sha256: `c41dabdb371446642e2caaa2a81a41549c50fe43749f661afde452db4574de2e`
- harness_fixed_sha256: `c36721521866978987f2dd97c3cc64687539c34726c67699716bb46cbb75222d`
- package_json_sha256: `f3ccd46701890ba6527eab42c3c470a51b7abd7b51a9a1a5234f605644d8568c`
- implementation_state: `src`, `.github` 없음; `docs/contracts`에 16개 fixed projection 존재
- ignored_paths: `node_modules`, `dist`, `coverage`, generated output, screenshot, Playwright/test artifact, `.cache`

## 리뷰 영역 요약

| area | last_reviewed_at | decision_summary | skipped_this_run | skip_reason |
| --- | --- | --- | --- | --- |
| frontend-runtime-build-tool | 2026-07-13 | React TypeScript Vite SPA | false | 최초 review |
| typescript-configuration | 2026-07-13 | 강화 strict | false | 최초 review |
| routing-boundary | 2026-07-13 | explicit hierarchical routes | false | 최초 review |
| state-management-server-cache | 2026-07-13 | local/Query/STOMP/client 분리 | false | 최초 review |
| api-client-error-auth | 2026-07-13 | fetch/generated/adapter/session | false | 최초 review |
| stomp-websocket-client | 2026-07-13 | session manager/snapshot resync | false | 최초 review |
| module-import-boundaries | 2026-07-13 | app→pages→features→entities→shared | false | 최초 review |
| component-architecture | 2026-07-13 | page→feature→view | false | 최초 review |
| styling-design-system-boundary | 2026-07-13 | CSS Modules/semantic token | false | 최초 review |
| frontend-hosting-cdn-proxy | 2026-07-13 | static same-site proxy | false | 최초 review |
| environment-runtime-config | 2026-07-13 | immutable artifact/runtime config | false | 최초 review |
| security-headers-public-secret | 2026-07-13 | edge-owned CSP/header/secret guard | false | 최초 review |
| client-observability-sourcemap | 2026-07-13 | vendor-neutral/private sourcemap | false | 최초 review |
| cicd | 2026-07-13 | PR→stage→approved prod | false | 최초 review |
| git-hook-mjs-harness | 2026-07-13 | shared MJS entrypoint | false | 최초 review |
| static-analysis-lint | 2026-07-13 | multi-tool hard gates | false | 최초 review |
| test-strategy-quality-gates | 2026-07-13 | Vitest/RTL/MSW/Playwright | false | 최초 review |
| contract-drift-gates | 2026-07-13 | fingerprint/temp regeneration | false | 최초 review |
| generated-client-mock-drift | 2026-07-13 | generated/MSW/schema fixture chain | false | 최초 review |
| be-contract-collaboration | 2026-07-13 | fixed source required | false | 최초 review |
| dependency-supply-chain-policy | 2026-07-13 | npm/audit/dependency review | false | 최초 review |
| release-preview-stage-prod | 2026-07-13 | same checksum promotion | false | 최초 review |

## 영역별 상세

### frontend-runtime-build-tool

- source_documents: BE spec, interview, `impl-fixed.md`, `ARCH-ADR-001`
- watched_paths: `package.json`, `vite.config.*`, `src/app`, `docs/architecture/fixed-*/impl-fixed.md`
- contract_sources: BE spec React client/same-site 전제
- ci_checks: `typecheck`, `build`
- source_fingerprint: impl fixed `1c4465f7...`
- implementation_paths: `src`, Vite config (현재 없음)
- implementation_fingerprint: absent
- decision_summary: React TypeScript Vite SPA, no SSR
- latest_result: pass; 구현 전 후보와 fixed 결정 일치

### typescript-configuration

- source_documents: `impl-fixed.md`, `ARCH-ADR-002`
- watched_paths: `tsconfig*.json`, `src`, generated type config
- contract_sources: OpenAPI/STOMP generated type (현재 fixed source 없음)
- ci_checks: `typecheck`
- source_fingerprint: impl fixed `1c4465f7...`
- implementation_paths: TypeScript config (현재 없음)
- implementation_fingerprint: absent
- decision_summary: 강화 strict와 generated type 포함
- latest_result: pass; scaffold handoff 필요

### routing-boundary

- source_documents: storyboard manifest, `impl-fixed.md`, `ARCH-ADR-003`
- watched_paths: route config, page manifest, `src/app`, `src/pages`
- contract_sources: auth/account/role spec
- ci_checks: route trace guard, component/E2E
- source_fingerprint: storyboard `c00e7a97...`, impl fixed `1c4465f7...`
- implementation_paths: route source (현재 없음)
- implementation_fingerprint: absent
- decision_summary: explicit nested route, auth/user/admin boundary
- latest_result: pass

### state-management-server-cache

- source_documents: BE server authority spec, `impl-fixed.md`, `ARCH-ADR-004`
- watched_paths: `src/features`, QueryClient, feature stores
- contract_sources: REST response와 STOMP snapshot/event
- ci_checks: unit/component/adapter test
- source_fingerprint: impl fixed `1c4465f7...`
- implementation_paths: state source (현재 없음)
- implementation_fingerprint: absent
- decision_summary: local/TanStack Query/STOMP/conditional Zustand 분리
- latest_result: pass

### api-client-error-auth

- source_documents: BE session/CSRF spec, `impl-fixed.md`, `ARCH-ADR-005`
- watched_paths: shared transport, generated client, feature API adapter
- contract_sources: fixed OpenAPI와 error model (현재 없음)
- ci_checks: adapter/contract/generated drift test
- source_fingerprint: impl fixed `1c4465f7...`
- implementation_paths: API source (현재 없음)
- implementation_fingerprint: absent
- decision_summary: fetch transport, generated client adapter, no JWT refresh
- latest_result: pass; fixed contract 전 구현 차단

### stomp-websocket-client

- source_documents: BE STOMP spec, `impl-fixed.md`, `ARCH-ADR-006`, `ARCH-ADR-019`
- watched_paths: connection manager, feature adapters, schema/fixture
- contract_sources: fixed STOMP destination/schema (현재 없음)
- ci_checks: STOMP adapter/schema/resync test
- source_fingerprint: impl fixed `1c4465f7...`
- implementation_paths: STOMP source (현재 없음)
- implementation_fingerprint: absent
- decision_summary: session manager, feature subscription, snapshot/version resync
- latest_result: pass; fixed schema 전 구현 차단

### module-import-boundaries

- source_documents: `impl-fixed.md`, `ARCH-ADR-007`
- watched_paths: `src`, dependency-cruiser config, MJS guard
- contract_sources: 없음
- ci_checks: dependency boundary, lint
- source_fingerprint: impl fixed `1c4465f7...`
- implementation_paths: `src` (현재 없음)
- implementation_fingerprint: absent
- decision_summary: app→pages→features→entities→shared
- latest_result: pass

### component-architecture

- source_documents: design baseline, storyboard, `impl-fixed.md`
- watched_paths: `src/pages`, `src/features`, `src/entities`, `src/shared/ui`, Storybook
- contract_sources: storyboard component patterns
- ci_checks: component test, Storybook build, a11y
- source_fingerprint: design `49a4875d...`, impl fixed `1c4465f7...`
- implementation_paths: component source (현재 없음)
- implementation_fingerprint: absent
- decision_summary: page→feature container→view, minimal provider
- latest_result: pass

### styling-design-system-boundary

- source_documents: approved design baseline, `impl-fixed.md`, `ARCH-ADR-008`, `ARCH-ADR-009`
- watched_paths: production styles/token/primitive, Stylelint, Storybook
- contract_sources: design baseline semantic token과 storyboard state
- ci_checks: Stylelint, token guard, Storybook, visual smoke
- source_fingerprint: design `49a4875d...`, impl fixed `1c4465f7...`
- implementation_paths: production style (현재 없음)
- implementation_fingerprint: absent
- decision_summary: CSS Modules, semantic token, foundation Storybook
- latest_result: pass; actual visual implementation은 foundation 소유

### frontend-hosting-cdn-proxy

- source_documents: BE same-site spec, `infra-fixed.md`, `ARCH-ADR-010`
- watched_paths: hosting/proxy/Docker/infra config, deployment workflow
- contract_sources: API/WebSocket path와 Origin (현재 없음)
- ci_checks: build, deploy smoke, WebSocket upgrade
- source_fingerprint: infra fixed `c41dabdb...`
- implementation_paths: infra config (현재 없음)
- implementation_fingerprint: absent
- decision_summary: static SPA와 same-site HTTPS proxy
- latest_result: pass; provider/path 미확정

### environment-runtime-config

- source_documents: `infra-fixed.md`, `ARCH-ADR-011`, `ARCH-ADR-018`
- watched_paths: runtime config schema/loader, deploy adapter, workflow
- contract_sources: public API/STOMP path keys (현재 없음)
- ci_checks: config schema, artifact checksum, deploy smoke
- source_fingerprint: infra fixed `c41dabdb...`
- implementation_paths: runtime/deploy config (현재 없음)
- implementation_fingerprint: absent
- decision_summary: same artifact와 runtime public config
- latest_result: pass

### security-headers-public-secret

- source_documents: BE security spec, `infra-fixed.md`
- watched_paths: proxy/hosting headers, env/config guard, CSP test
- contract_sources: OAuth origin, CSRF/WebSocket Origin (일부 미확정)
- ci_checks: public secret guard, header/CSP smoke
- source_fingerprint: infra fixed `c41dabdb...`
- implementation_paths: security header/config (현재 없음)
- implementation_fingerprint: absent
- decision_summary: entrypoint 단일 소유, report-only→enforce
- latest_result: pass; OAuth/HSTS 상세 후속 검토

### client-observability-sourcemap

- source_documents: `infra-fixed.md`
- watched_paths: observability adapter, Vite sourcemap, upload/deploy workflow
- contract_sources: privacy/retention policy (현재 없음)
- ci_checks: sourcemap private upload/public exclusion, release tag
- source_fingerprint: infra fixed `c41dabdb...`
- implementation_paths: observability config (현재 없음)
- implementation_fingerprint: absent
- decision_summary: vendor-neutral adapter와 private sourcemap
- latest_result: pass; vendor 미확정

### cicd

- source_documents: `harness-fixed.md`, `ARCH-ADR-018`
- watched_paths: `.github/workflows`, deploy adapter, package scripts
- contract_sources: contract drift source와 deployment endpoint
- ci_checks: all required checks, stage/prod gate
- source_fingerprint: harness fixed `c3672152...`
- implementation_paths: `.github` (현재 없음)
- implementation_fingerprint: absent
- decision_summary: PR→main artifact→stage→approved production
- latest_result: pass; scaffold/infra handoff 필요

### git-hook-mjs-harness

- source_documents: `harness-fixed.md`, `ARCH-ADR-014`
- watched_paths: `.husky`, guard/helper `.mjs`, fixtures
- contract_sources: contract fingerprint inputs
- ci_checks: guard fixture, pre-commit/pre-push/CI reuse
- source_fingerprint: harness fixed `c3672152...`, package `f3ccd467...`
- implementation_paths: package has Husky only; guard 없음
- implementation_fingerprint: package `f3ccd467...`
- decision_summary: staged/changed/all shared MJS entrypoint
- latest_result: pass with documented implementation drift

### static-analysis-lint

- source_documents: `harness-fixed.md`, `ARCH-ADR-013`
- watched_paths: ESLint/Prettier/dependency-cruiser/Stylelint/Knip config
- contract_sources: generated paths와 design token source
- ci_checks: typecheck, lint, format, boundary, style
- source_fingerprint: harness fixed `c3672152...`
- implementation_paths: config 없음
- implementation_fingerprint: absent
- decision_summary: multi-tool Hard gate, Knip 단계화
- latest_result: pass; scaffold handoff 필요

### test-strategy-quality-gates

- source_documents: storyboard, `harness-fixed.md`, `ARCH-ADR-015`
- watched_paths: Vitest/Testing Library/MSW/Playwright config와 tests
- contract_sources: API/STOMP schema/fixture, issue metadata
- ci_checks: unit/component/adapter/conditional E2E/visual
- source_fingerprint: storyboard `c00e7a97...`, harness fixed `c3672152...`
- implementation_paths: test config/source 없음
- implementation_fingerprint: absent
- decision_summary: 계층별 test 책임과 retry 0
- latest_result: pass

### contract-drift-gates

- source_documents: BE interface stability spec, `harness-fixed.md`, `ARCH-ADR-016`
- watched_paths: `docs/contracts`, generation/fingerprint scripts, cache manifest
- contract_sources: fixed OpenAPI/STOMP/BE hash (fixed projection 없음)
- ci_checks: source fingerprint, temp regeneration, schema fixture
- source_fingerprint: harness fixed `c3672152...`
- implementation_paths: `docs/contracts` 없음
- implementation_fingerprint: absent
- decision_summary: full contract chain drift Hard gate
- latest_result: pass; feature contract 구현 차단 상태

### generated-client-mock-drift

- source_documents: `harness-fixed.md`, `ARCH-ADR-016`
- watched_paths: generated client/type, MSW handlers, fixtures, generator config
- contract_sources: fixed OpenAPI/STOMP (현재 없음)
- ci_checks: temp regeneration diff, mock coverage, schema test
- source_fingerprint: harness fixed `c3672152...`
- implementation_paths: generated/mock 없음
- implementation_fingerprint: absent
- decision_summary: generated code와 mock을 동일 source에 연결
- latest_result: pass; fixed source 후 도입

### be-contract-collaboration

- source_documents: BE spec/PRD, `impl-fixed.md`, `create-trd-handoff.md`
- watched_paths: `.cache/spec-read`, `.cache/prd-read`, `docs/contracts`, contract projection metadata
- contract_sources: BE master spec commit `a552e067...`, fixed 계약 없음
- ci_checks: freshness/fingerprint/contract status
- source_fingerprint: spec sha `d0309e90...`
- implementation_paths: contract projection 없음
- implementation_fingerprint: absent
- decision_summary: fixed source 없으면 추정 금지
- latest_result: pass; `sync-fe-contracts` 후 재검토

### dependency-supply-chain-policy

- source_documents: `harness-fixed.md`, `ARCH-ADR-012`, `ARCH-ADR-017`
- watched_paths: `package.json`, lockfile, npm config, dependency workflow
- contract_sources: registry/license policy
- ci_checks: npm ci, audit high, dependency review/conditional license
- source_fingerprint: package `f3ccd467...`, harness fixed `c3672152...`
- implementation_paths: lockfile/CI 없음
- implementation_fingerprint: package `f3ccd467...`
- decision_summary: pinned npm/lockfile, audit와 no auto force/merge
- latest_result: pass with documented implementation drift

### release-preview-stage-prod

- source_documents: `infra-fixed.md`, `harness-fixed.md`, `ARCH-ADR-018`
- watched_paths: workflow, deploy adapter, runtime config, artifact metadata
- contract_sources: hosting/BE release compatibility (현재 미확정)
- ci_checks: checksum, stage smoke, production approval, rollback artifact
- source_fingerprint: infra `c41dabdb...`, harness `c3672152...`
- implementation_paths: deployment config 없음
- implementation_fingerprint: absent
- decision_summary: conditional preview, automatic stage, approved prod same checksum
- latest_result: pass; provider/runbook 후 재검토

## 공통 생략 조건

다음이 모두 같을 때만 다음 review에서 해당 area를 생략할 수 있다.

- source document와 관련 fixed/ADR fingerprint
- design/storyboard 또는 interface contract
- 관련 source/config/dependency/lockfile
- CI check와 deploy/hosting policy
- 기존 미확정 상태

## 공통 재검토 조건

- BE spec/PRD/storyboard/design baseline/fixed contract 변경
- 관련 FE source, package, tool config 또는 dependency 변경
- routing/state/API/STOMP/import/style/component boundary 변경
- hosting/proxy/runtime config/security header/observability 변경
- required check, hook, test, contract/generated/mock drift 정책 변경
- package manager/lockfile/engine/dependency policy 변경
- 미확정 항목 확정
- fixed 문서와 accepted ADR 선택·상태 불일치
