# Architecture Reconfirmation 20260723

## Input and Decision

- BE spec/PRD commit: `b939d5df32342422f98e3ac603fa32532c7424fb`
- spec sha256: `6ac09a695776736f72bd683785d6e8b9c343f4af5f86545bd1964218cd7a7f10`
- PRD manifest sha256: `33e482133073c19b76655d3b390192e7270e5fcd8430bbcc5d8cb5c6f7f348ef`
- contract inputs: 16 fixed FE projections, BE negotiation session `completed`
- user decision: 기존 전역 FE 선택을 유지하면서 최신 계약을 반영한 재확정 loop를 진행한다.

## Reconfirmed Decisions

- React + TypeScript + Vite SPA, hierarchical route, local/Query/STOMP state ownership, CSS Modules/token, same-site deployment와 기존 CI/CD 선택은 유지한다.
- REST와 STOMP는 canonical registry/manifest/fixture에서 생성된 closed schema만 소비한다. 수기 union, 자유형 mock, payload 추정은 허용하지 않는다.
- schema/Ajv 검증은 query cache나 game reducer 전에 수행한다. snapshot과 replay `stateAfter`는 원자 교체하며 FE가 카드 효과, FEN, outcome 좌표를 재계산하지 않는다.
- catalog fingerprint·collection/deck revision·viewer-redacted public/private projection을 feature boundary에서 보존한다.

## Alternatives and Outcome

- 기존 `fixed-20260713`만 유지: 최신 계약의 source trace와 drift gate가 비어 있어 제외했다.
- 계약 내용을 feature TRD에서만 해석: 전역 reducer/adapter/harness 경계가 feature마다 달라질 위험으로 제외했다.
- 새 전역 기술/ADR 도입: 기존 ADR-005, 006, 016, 019가 선택을 이미 소유하므로 제외했다.

## Review Loop

- loop: 1
- result: `review-pass`
- new ADR: 없음
- unresolved: canonical OpenAPI/STOMP artifact 위치와 generation command, 실제 hosting/runtime config 값
