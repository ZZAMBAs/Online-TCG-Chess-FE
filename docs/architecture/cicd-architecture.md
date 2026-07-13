# CI/CD Architecture

## 목적

재현 가능한 설치, PR 검증, 불변 artifact 승격과 release 차단 조건을 정의한다.

## 원천 산출물

- `docs/architecture/interview-20260713/summary.md`
- `docs/architecture/frontend-architecture.md`
- `docs/architecture/frontend-infrastructure.md`
- 관련 ADR: `ARCH-ADR-012`~`ARCH-ADR-018`

## 브랜치와 머지 정책

- `main` 직접 push를 금지하고 작업 branch PR을 사용한다.
- required check와 unresolved review thread 해소 뒤 merge한다.
- stale check와 conflict가 있으면 최신 기준으로 재검증한다.
- 기본 merge 방식은 squash merge다.
- emergency bypass는 관리자 승인, 사유와 후속 issue를 요구한다.

## Package Manager와 Lockfile 정책

- npm을 사용하고 Node LTS major와 npm 버전을 고정한다. (`ARCH-ADR-012`)
- `engines`, `packageManager`, Node version file을 일치시킨다.
- `package-lock.json`을 commit하고 CI는 `npm ci`만 사용한다.
- 정확한 version은 scaffold 시 공식 지원 관계를 확인해 정한다.

## Required Checks

- install/lockfile
- typecheck
- lint/format/import/style/boundary guard
- unit/component/adapter/contract test
- contract/generated/mock drift
- build
- dependency audit/review
- issue 조건에 따른 E2E/visual smoke

## Typecheck

- 강화 strict TypeScript 전체 검사를 Hard gate로 둔다.
- generated type도 포함한다.

## Lint와 Format

- type-aware ESLint, Prettier check, import sorting, Stylelint를 Hard gate로 둔다.
- dependency-cruiser와 custom `.mjs` guard로 module/token boundary를 검사한다. (`ARCH-ADR-013`)
- Knip과 warning budget은 안정화 뒤 차단 수준을 높인다.

## Unit/Component Test

- Vitest unit과 Testing Library component test는 Hard gate다. (`ARCH-ADR-015`)
- MSW REST adapter와 STOMP fake transport/schema fixture test를 포함한다.

## E2E Test

- issue의 `e2e_required`가 true면 Playwright를 Conditional required check로 실행한다.
- foundation 또는 지정 issue의 `visual_states`에 desktop/mobile visual smoke를 실행한다.
- retry는 기본 0이며 별도 diagnostic 반복이 required result를 성공으로 바꾸지 않는다.

## Build 검증

- Vite production build와 artifact manifest/checksum 생성을 Hard gate로 둔다.
- Storybook 도입 뒤 Storybook build도 Hard gate다.
- bundle 크기와 route chunk를 기록하고 baseline 뒤 regression gate를 적용한다.

## Contract Drift Check

- BE spec/PRD와 fixed contract projection fingerprint를 검사한다. (`ARCH-ADR-016`)
- fixed 계약이 없으면 endpoint/payload 기반 feature 구현을 차단한다.

## Generated Client 검증

- CI temp directory에 client/type을 재생성하고 committed output과 diff한다.
- 생성 command와 generator version을 고정한다.
- generated file 직접 수정을 차단한다.

## MSW Mock Drift 검증

- handler는 generated contract type을 사용한다.
- fixed endpoint 누락과 obsolete mock을 검사한다.
- fixture는 schema와 adapter test를 통과해야 한다.

## Dependency와 Supply-chain 검사

- `npm audit --audit-level=high`를 Hard gate로 둔다. (`ARCH-ADR-017`)
- 가능한 환경에서 GitHub dependency review로 PR 신규 취약 dependency를 차단한다.
- license와 registry signature 검사는 정책·지원 확인 뒤 Conditional gate로 적용한다.
- 자동 `audit fix --force`와 자동 dependency merge를 금지한다.
- 예외는 advisory id, 영향, owner, expiry, follow-up issue를 요구한다.

## 테스트 리포트와 메트릭 검사

- Vitest JUnit/coverage와 CI summary를 생성한다.
- `skip`, `only`, 예상 test 수 감소를 검사한다.
- coverage는 foundation baseline 뒤 하락을 Hard gate로 전환한다.
- duration과 failure rate는 baseline 뒤 Conditional gate로 관리한다.

## Preview/Stage/Prod 배포

- PR은 기본적으로 검증만 하고 필요한 경우에만 preview를 만든다.
- main commit에서 production artifact를 한 번 생성한다. (`ARCH-ADR-018`)
- stage에 자동 배포해 smoke를 통과한 동일 artifact만 production 후보가 된다.
- production은 environment approval 뒤 승격한다.

## Release Gates

- required checks 통과
- stage deployment와 smoke 통과
- runtime config schema 통과
- security header/CSP 검사 통과
- API/STOMP connectivity smoke 통과
- production environment 승인

## Artifact와 Version

- artifact에 commit, release id, checksum을 기록한다.
- 환경별 rebuild를 금지한다.
- 실패 trace/screenshot은 최소 조사 기간만 보존하고 성공 capture는 보존하지 않는다.

## Rollback 정책

- 이전에 검증된 동일 artifact와 당시 호환 runtime config를 재배포한다.
- rollback을 위해 새 build를 만들지 않는다.
- BE와의 상세 호환 순서와 migration rollback은 release runbook에서 확정한다.

## Secret 처리

- CI secret은 environment scope와 최소 권한을 사용한다.
- public runtime config와 secret을 분리한다.
- log와 artifact에 credential을 출력하지 않는다.

## 후속 스킬 연계

- architecture fixed 승인 뒤 scaffold 설정 반영
- 계약 협상/`sync-fe-contracts`
- foundation baseline 측정
- 운영 deployment/rollback runbook

## 미확정 사항

- GitHub dependency review 사용 가능 여부
- Node/npm과 tool exact version
- GitHub environment 권한과 reviewer 수
- coverage, duration, bundle, artifact retention 수치
- hosting adapter와 BE 동시 release 순서
