# Contract Schema Closure FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/contract-schema-closure/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- AuthSession, OAuth result, RestError, matchmaking state, ViewerGameState, 19 GameEvent payload, replay outcome, trust/admin union은 canonical closed schema를 사용한다.
- 모든 object와 discriminated union은 schema version과 닫힌 field 집합을 따른다. unknown variant/field와 schema 불일치는 정상 데이터가 아니다.
- snapshot/stateAfter는 viewer-redacted state schema를 사용하고 원자 교체한다. replay에서 live-only capability, receipt, connection metadata를 포함하지 않는다.
- REST/STOMP registry, manifest와 fixture fingerprint가 wire contract의 canonical source다.

## FE Consumption Notes

- generated TypeScript와 exhaustive switch를 사용한다.
- schema 검증 실패는 query cache/reducer 전에 fatal drift로 차단한다.

## Excluded From FE Projection

- BE schema 생성·검증 파이프라인, persistence와 내부 DTO 조립.
