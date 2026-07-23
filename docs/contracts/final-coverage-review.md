# Final Coverage Review FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/final-coverage-review/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- canonical contract surface는 63개 REST operation과 STOMP CONNECT/SUBSCRIBE/SEND/server channel, auth/cookie/CSRF, 공통 오류, matchmaking, game, chat, replay, community, identity, trust/admin을 포함한다.
- 모든 소비자는 canonical manifest와 fixture, generated schema를 기준으로 하며 private tail loss, unknown definition, privacy leakage와 contract drift를 허용하지 않는다.

## FE Consumption Notes

- generated OpenAPI/TypeScript/Ajv, MSW, fake STOMP와 Playwright의 입력 source를 canonical manifest/fixture로 고정한다.
- FE 해석: 이 문서는 개별 topic 계약의 coverage 기준이며 새 endpoint를 추가하는 해석은 하지 않는다.

## Excluded From FE Projection

- final coverage 검토 절차, 양 repo sync 실행 순서와 BE 구현 계약 생성.
