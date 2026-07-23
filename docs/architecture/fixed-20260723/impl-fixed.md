# FE Implementation Architecture Fixed

## Status and Sources

- status: fixed
- fixed_date: 20260723
- interview: `docs/architecture/interview-20260723/summary.md`
- design source: `docs/design/design-baseline.md` (`approved`)
- contract source: `docs/contracts/*.md` (16 fixed projections)

## Runtime, Route and Module Boundaries

- React + TypeScript + Vite SPA, explicit hierarchical React Router, `app → pages → features → entities → shared` import direction을 유지한다. (`ARCH-ADR-001`~`ARCH-ADR-003`, `ARCH-ADR-007`)
- page는 route 조합, feature container는 query/store/command 연결, entity/shared view는 props/event만 소유한다. 일반 사용자·관리자·인증 boundary와 error boundary를 분리한다.
- CSS Modules와 semantic token을 사용하며 storyboard CSS를 production에 import하지 않는다. (`ARCH-ADR-008`, `ARCH-ADR-009`)

## State and Contract Consumption

- local UI는 React, REST server state는 TanStack Query, game snapshot/event/pending은 feature reducer/store가 소유한다. (`ARCH-ADR-004`)
- common fetch transport → generated client → feature adapter → Query 순서를 유지한다. same-site credential/CSRF/error mapping은 transport 책임이다. (`ARCH-ADR-005`)
- session-scope STOMP manager는 connection/reconnect/resync만 소유하고 feature adapter가 subscription/command를 소유한다. (`ARCH-ADR-006`)
- canonical manifest/registry/fixture의 generated closed schema와 Ajv 검증을 cache/reducer 이전에 적용한다. unknown field/variant, schema mismatch, fingerprint mismatch는 fatal contract drift다. (`ARCH-ADR-016`, `ARCH-ADR-019`)
- viewer-redacted snapshot과 replay `stateAfter`는 원자 교체한다. duplicate/version gap은 각각 ignore/resync로 처리하며, public transition·actor-private augmentation·local selection draft·pending overlay를 분리한다.
- FE는 card effect, FEN legality, outcome 좌표를 재계산하거나 현재 card handler로 replay를 재해석하지 않는다. cardId/version, catalog fingerprint, collection/deck revision은 서버 계약값으로 소비한다.

## Hard Constraints and Handoff

- fixed projection 없이 endpoint, destination, payload 또는 schema를 추정하지 않는다. generated code를 직접 수정하지 않는다.
- TRD는 이 문서의 runtime/state/transport/module/style 정책을 재결정하지 않으며, feature별 query key·route·error mapping·visual state만 구체화한다.
- 미확정: canonical OpenAPI/STOMP artifact path, generation command, runtime path/config, font/artwork asset.
