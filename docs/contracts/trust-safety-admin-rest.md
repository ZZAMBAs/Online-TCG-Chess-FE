# Trust Safety Admin REST FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/trust-safety-admin-rest/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- 모든 응답은 `schemaVersion:"1"`의 closed schema다. mutation은 CSRF와 persistent `Idempotency-Key`를 요구하며 exact replay와 `COMMAND_CONFLICT`를 구분한다.
- 일반 user target은 server-issued opaque `subjectRef`로만 지정한다. capability가 없는 self/withdrawn/expired target은 action을 제공하지 않는다.
- block은 cursor page와 revision을 사용한다. report target은 `CHAT_MESSAGE`, `COMMUNITY_POST`, `USER_PROFILE` union이며 reason/detail 제한을 따른다.
- admin report case, raw evidence, moderation, sanction, forbidden-word, card read-only, announcement endpoint는 role/account state와 closed unions를 따른다.
- raw evidence/admin card/detail query는 prefetch, automatic retry, focus/reconnect refetch를 사용하지 않으며 role loss/logout/session rotation 때 cache를 제거한다.
- server access matrix와 conflict response가 최종 권위다. identity, raw evidence, internal account ID와 민감 admin 정보는 허용되지 않은 view에 노출하지 않는다.

## FE Consumption Notes

- public/admin layout과 query cache를 분리한다.
- subjectRef capability로 action을 표시하되 서버 거부를 정상적으로 처리한다.
- conflict에서는 draft를 유지하고 refetch하며 자동 merge/retry하지 않는다.

## Excluded From FE Projection

- evidence 저장/expiry cleanup, sanction/moderation transaction, audit와 repository 구현.
