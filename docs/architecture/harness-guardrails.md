# Harness Guardrails

## 목적

architecture, contract, design과 test 규칙을 local hook과 CI에서 재사용 가능한 gate로 강제한다.

## Hard Gate

- npm lockfile 재현과 pinned engine
- 강화 TypeScript typecheck
- type-aware ESLint, Prettier, import sorting
- dependency-cruiser module boundary
- Stylelint와 token/style `.mjs` guard
- Vitest unit/component/adapter/contract test
- Vite build와 도입 뒤 Storybook build
- OpenAPI/STOMP fingerprint와 generated/mock/schema drift
- high/critical dependency audit
- fixed contract가 필요한 feature의 contract 존재·상태
- `skip`/`only`, generated direct edit, public secret 금지 guard

## Conditional Gate

- issue의 `e2e_required`에 따른 Playwright
- issue의 `visual_states`에 따른 visual smoke
- Knip unused export/dependency 검사
- coverage, duration, bundle regression
- GitHub dependency review, license와 signature 검사
- CSP report-only violation과 deployment smoke

## Advisory 도구

- baseline 전 coverage, bundle, Web Vitals, duration trend
- moderate 이하 dependency advisory
- allowlist 안정화 전 warning/Knip report

## TypeScript 강제 규칙

- strict 추가 옵션과 `src` alias를 설정한다.
- `any`, unchecked assertion과 generated type 예외를 무근거 허용하지 않는다.
- generated code를 별도 skip하지 않고 compile한다.

## ESLint와 Import Boundary

- type-aware project service를 사용한다.
- jsx a11y, hooks, TanStack Query 규칙을 적용한다.
- import sorting과 계층 역방향·feature cross import를 차단한다.
- architecture rule과 일반 code style rule id를 구분한다.

## Formatting과 Style Guard

- Prettier check를 CI에서 실행하고 hook에서는 staged file만 format한다.
- Stylelint는 CSS syntax/module rule을 검사한다.
- `.mjs` guard는 raw token bypass, 금지 inline style, storyboard CSS production import를 검사한다.
- runtime coordinate/size exception은 중앙 allowlist와 CSS variable 전달 형식으로 제한한다.

## Git Hook mjs Guard

- pre-commit은 staged Prettier/ESLint/Stylelint와 빠른 guard를 실행한다. (`ARCH-ADR-014`)
- pre-push는 typecheck, 영향 test, boundary와 contract fingerprint를 실행한다.
- CI는 같은 entrypoint의 `--all` mode를 사용한다.
- 로컬 `--no-verify`는 허용하되 CI 우회는 허용하지 않는다.

## MJS Guard 입력/출력/Fixture 정책

- 입력: lint-staged file argument, 명시적 `--files`, 전체 `--all`
- ignore: generated, `dist`, coverage, snapshot, Playwright artifact, vendored file
- 출력: rule id, file, reason, remediation hint
- exit: success `0`, rule violation `1`, tool/config error `2`
- test: pass/fail fixture와 expected output을 둔다.

## Unit/Component Test Guard

- public behavior를 검증하고 private implementation snapshot 남용을 피한다.
- shared primitive는 variant, keyboard/focus, disabled/loading과 a11y를 검증한다.
- REST는 MSW, STOMP는 fake transport/schema fixture를 사용한다.

## E2E Guard

- route, auth boundary, 핵심 사용자 흐름과 지정 visual state를 검증한다.
- required retry 기본값은 0이다.
- 실패 trace/screenshot만 제한 보존하고 성공 local capture는 삭제한다.

## Contract Drift Guard

- fixed source fingerprint를 확인한다.
- temp generation diff로 generated client/type을 검증한다.
- MSW endpoint coverage와 obsolete mock을 검사한다.
- STOMP JSON Schema와 fixture, Ajv runtime validator를 같은 원천에 연결한다. (`ARCH-ADR-019`)
- source가 fixed가 아니면 임의 생성하지 않고 실패한다.

## Dependency와 Supply-chain Guard

- `npm ci`, lockfile, engine/packageManager 일치를 검사한다.
- `npm audit --audit-level=high`를 실행한다.
- 자동 force fix와 자동 merge를 금지한다.
- 신규 direct dependency는 목적, 대안, bundle, license, maintenance 근거를 요구한다.
- exception에는 advisory, 영향, owner, expiry와 follow-up issue가 필요하다.

## CI Required Check

- PR check는 install, static, test, contract, build, dependency를 분리하되 필수 상태가 명확해야 한다.
- E2E/visual conditional 여부는 issue metadata에서 결정한다.
- stage smoke와 production approval은 release gate다.

## 테스트 실행 리포트와 메트릭

- JUnit, coverage, Playwright HTML/trace와 CI summary를 생성한다.
- `skip`, `only`, test count 감소를 검사한다.
- flaky diagnostic 반복은 required result를 성공으로 덮지 않는다.
- baseline 뒤 coverage 하락과 duration 급증을 차단한다.

## Artifact 보존과 정리 정책

- main artifact와 release checksum은 rollback 가능한 기간 보존한다.
- 실패 report/trace/screenshot은 조사 최소 기간만 보존한다.
- 성공 E2E capture와 중간 generation output은 폐기한다.
- 정확한 일수는 운영 비용 확인 뒤 정한다.

## 도입 전 PoC 항목

- tool version 간 TypeScript/ESLint/Vite/Vitest 호환성
- dependency-cruiser와 path alias 경계
- Stylelint CSS Modules와 token guard fixture
- OpenAPI temp generation determinism
- STOMP JSON Schema→TypeScript/Ajv pipeline
- OAuth 흐름과 CSP/추가 isolation header 호환성

## 후속 스킬 연계

- fixed 승인 뒤 architecture scaffold
- foundation issue의 token/primitive/Storybook과 baseline
- 계약 협상/`sync-fe-contracts`
- feature별 TDD와 conditional `e2e-test`
- `security-review`

## 미확정 사항

- exact tool/version과 script name
- generated/mock path와 fixed contract source
- coverage/duration/bundle/retention threshold
- GitHub dependency/security feature 사용 가능 여부
