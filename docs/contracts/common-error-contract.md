# Common Error Contract FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/common-error-contract/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- REST, STOMP fatal, STOMP application 오류는 transport별 닫힌 schema를 사용하며 공통 필드는 `schemaVersion`, `errorCode`, `message`, `traceId`다.
- validation 오류는 조건부 field error를 포함할 수 있다. FE는 `errorCode`와 상태 code를 기준으로 의미를 결정하고 `message`를 권위 문구로 취급하지 않는다.
- 오류 code registry의 범주는 field/global validation, auth, permission/restriction, not-found, conflict/resync, rate-limit, internal fallback과 fatal contract drift다.
- rate limit은 `Retry-After`/retry metadata를 따르며 auth·mutation 오류를 임의 재전송하지 않는다.

## FE Consumption Notes

- 공통 normalizer가 REST와 STOMP 오류를 typed error로 변환한다.
- expected error는 feature 상태로, fatal drift는 reducer와 reconnect 전에 차단한다.

## Excluded From FE Projection

- 서버 오류 registry 운영, trace/observability 저장과 backend 검증 구현.
