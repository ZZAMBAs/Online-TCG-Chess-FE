# Game State Sync FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/game-state-sync/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- game STOMP destination, 권한, command/event/snapshot envelope와 version은 canonical schema를 따른다.
- public/private projection은 viewer 권한에 맞게 merge하며 duplicate는 무시하고 version gap은 resync 대상으로 처리한다.
- snapshot은 원자 교체한다. connection 재수립·deadline·permission denied·fatal schema error는 서로 다른 상태다.
- session rotation과 permission change 뒤에는 기존 connection을 추정하지 않고 재검증·resync한다.

## FE Consumption Notes

- session-scope STOMP manager는 자기 connection/reconnect/resync만 관리한다.
- reducer 앞에서 Ajv 검증 후 `ready`, `reconnecting`, `resyncing`, `permission_denied`, `fatal_schema_error`를 구분한다.

## Excluded From FE Projection

- STOMP broker, server projection 생성과 game persistence 구현.
