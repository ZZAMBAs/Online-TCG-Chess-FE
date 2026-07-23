# FE Harness Architecture Fixed

## Status and Sources

- status: fixed
- fixed_date: 20260723
- related ADR: `ARCH-ADR-002`, `ARCH-ADR-012`~`ARCH-ADR-019`
- contract source: `docs/contracts/contract-schema-closure.md`, `contract-fixture.md`, `final-coverage-review.md`

## Hard Gates

- TypeScript, type-aware lint, formatting/import/style guard, import boundary, unit/component/adapter/contract test, build, high/critical audit와 lockfile 재현을 유지한다.
- canonical manifest/registry/fixture fingerprint, generated type/client, MSW/fake STOMP, Ajv schema의 연쇄 검증을 contract drift hard gate로 둔다.
- schema privacy validation, unknown union/definition, generated direct edit, public secret, skipped focused test는 CI 통과 상태가 될 수 없다.

## Conditional and Advisory Gates

- issue의 `e2e_required`와 `visual_states`에 따라 Playwright/visual smoke를 실행한다. coverage/duration/bundle/unused 검사는 foundation baseline 뒤 강화한다.
- source artifact path와 generation command가 제공되기 전에는 임의 generator나 fixture를 만들지 않고, 해당 부족을 contract-source blocker로 보고한다.

## CI/CD

- PR은 static → unit/component/contract → build → conditional E2E 순서로 검증한다.
- main artifact는 한 번 build하고 stage smoke 후 같은 checksum을 production 승인으로 승격한다. 성공 capture는 삭제하고 실패 artifact만 최소 기간 보존한다.
