# FE Harness Architecture Fixed

## 상태와 원천

- status: fixed
- fixed_date: 20260713
- 상세 근거: `docs/architecture/cicd-architecture.md`, `docs/architecture/harness-guardrails.md`
- 관련 ADR: `ARCH-ADR-002`, `ARCH-ADR-012`~`ARCH-ADR-019`

## Package와 Branch

- npm, committed lockfile, `npm ci`, pinned Node/npm을 사용한다. (`ARCH-ADR-012`)
- `main` 직접 push를 금지하고 PR required check와 squash merge를 사용한다.
- 정확한 version과 reviewer 수는 scaffold/저장소 권한 확인 뒤 기록한다.

## Hard Gate

- 강화 TypeScript typecheck
- type-aware ESLint, Prettier, import sorting
- dependency-cruiser import boundary
- Stylelint와 token/style `.mjs` guard (`ARCH-ADR-013`)
- Vitest unit/component/adapter/contract test
- Vite build와 도입 뒤 Storybook build
- fixed contract fingerprint, generated/mock/schema drift (`ARCH-ADR-016`)
- high/critical dependency audit와 lockfile 재현 (`ARCH-ADR-017`)
- `skip`/`only`, generated direct edit, public secret 금지

## Conditional와 Advisory

- issue `e2e_required`에 따른 Playwright
- issue `visual_states`에 따른 visual smoke
- allowlist 안정화 뒤 Knip
- foundation baseline 뒤 coverage, duration, bundle regression
- repository 지원 시 dependency review, 정책 확정 뒤 license/signature 검사
- baseline 전 지표와 moderate 이하 advisory는 보고한다.

## Git Hook MJS

- pre-commit은 staged fast check, pre-push는 changed-scope check, CI는 같은 entrypoint의 full check를 실행한다. (`ARCH-ADR-014`)
- entrypoint는 `--files/--all`, 중앙 ignore, rule id·remediation과 exit `0/1/2`를 제공한다.
- pass/fail fixture와 expected output을 둔다.
- local `--no-verify`는 가능하지만 CI 우회는 불가하다.

## Test Strategy

- Vitest unit, Testing Library component, MSW REST adapter, fake STOMP transport/schema fixture를 Hard gate로 둔다. (`ARCH-ADR-015`)
- Playwright는 route와 지정 browser/visual flow를 검증한다.
- required retry 기본값은 0이며 diagnostic 반복이 required 결과를 성공으로 바꾸지 않는다.
- 실패 artifact만 최소 조사 기간 보존하고 성공 capture는 삭제한다.

## Contract와 Runtime Schema

- source fingerprint, temp regeneration diff, generated client/type, MSW mock, STOMP fixture를 연쇄 검증한다. (`ARCH-ADR-016`)
- fixed JSON Schema와 Ajv로 주요 STOMP message를 검증한다. (`ARCH-ADR-019`)
- source가 fixed가 아니면 생성·구현을 실패시키고 임의 schema를 만들지 않는다.

## Supply Chain

- `npm audit --audit-level=high`를 Hard gate로 둔다.
- force fix와 update bot auto merge를 금지한다.
- exception은 advisory, 영향, owner, expiry와 follow-up issue를 요구한다.

## CI/CD

- PR: install → static → unit/component/contract → build → 조건부 E2E
- main: production artifact 1회 build, checksum/release metadata 기록
- stage: 자동 deploy와 runtime config/header/API/STOMP smoke
- production: 같은 checksum artifact를 environment 승인 뒤 승격 (`ARCH-ADR-018`)
- rollback: 이전 검증 artifact와 호환 config를 재배포

## 미확정

- exact tool version과 npm script
- fixed contract/generated/mock path
- coverage/duration/bundle/retention threshold
- GitHub dependency review와 environment 권한
- hosting adapter와 BE 동시 release runbook
