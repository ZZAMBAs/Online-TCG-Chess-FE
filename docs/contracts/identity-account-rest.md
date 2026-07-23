# Identity Account REST FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/identity-account-rest/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- profile, access status, settings, notification inbox와 match-history/card/deck 조회는 각 fixed REST schema를 사용한다.
- settings mutation은 revision/conflict를 반환하며 stale local value를 자동 덮어쓰거나 재전송하지 않는다.
- notification item은 closed discriminated union이고 required/optional 보관 및 announcement 결과에 따른 노출 규칙을 따른다.
- session rotation, logout, withdrawal 뒤 `/me/**` 민감 cache를 폐기한다.

## FE Consumption Notes

- 마이페이지는 profile/access-status/settings/notifications/history/card/deck query를 독립적으로 조합한다.
- notification plain text는 HTML로 해석하지 않는다.

## Excluded From FE Projection

- account/notification transaction, 보관 cleanup과 repository 구현.
