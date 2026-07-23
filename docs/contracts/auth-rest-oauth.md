# Auth REST OAuth FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/auth-rest-oauth/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- 가입·OAuth onboarding은 현재 consent version과 정확히 일치해야 한다. 충돌은 `409 REGISTRATION_CONFLICT`, consent 불일치는 `409 CONSENT_VERSION_OUTDATED`다.
- local login 성공은 session projection을 반환하고 session을 회전한다. 잘못된 자격 증명은 `401 INVALID_CREDENTIALS`, 잠금은 `429 ACCOUNT_LOCKED`다. logout은 `204`다.
- email verification, password reset, reactivation token은 URL fragment로 전달하고 FE는 읽은 즉시 history에서 제거한 뒤 body로 단회 제출한다.
- OAuth callback은 항상 `/auth/oauth/complete`로 이동한다. completion route는 `GET /api/v1/auth/oauth/result`를 cache/retry 없이 한 번 소비하고 closed outcome으로 분기한다.
- bootstrap 전 route guard는 redirect하지 않는다. `UNVERIFIED`, `SUSPENDED`, `WITHDRAWN`은 각각 제한된 허용 route를 따른다.
- withdrawal/reactivation은 기존 account identity와 기록을 유지하며, 관련 session·STOMP가 무효화될 수 있다.

## FE Consumption Notes

- session provider와 route guard가 rotation·logout·reset·withdrawal 뒤 재bootstrap한다.
- OAuth result는 비캐시 단회 consumer로 onboarding/login/collision/recovery를 mapping한다.
- FE 해석: auth mutation은 임의 자동 retry하지 않는다.

## Excluded From FE Projection

- provider token 처리, proof/token 저장·hashing, transaction/concurrency 및 SMTP 내부 구현.
