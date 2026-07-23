# Auth Cookie CSRF FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/auth-cookie-csrf/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- REST는 same-origin 상대 경로와 `credentials: "same-origin"`을 사용한다.
- CSRF는 `GET /api/v1/auth/csrf`에서 `{schemaVersion:"1",token}`으로 bootstrap하며 `no-store`다. token은 메모리에만 보관하고 mutation REST와 STOMP CONNECT의 `X-CSRF-TOKEN` header로만 전달한다.
- `GET /api/v1/auth/session`은 anonymous도 `200 {authenticated:false}`를 반환한다. 보호 API의 session 부재·만료는 `401 UNAUTHENTICATED`다.
- WebSocket은 `/ws` native handshake를 사용하며 SockJS와 자동 reconnect를 사용하지 않는다. 인증·CSRF·권한 오류는 `ERROR` frame 후 연결을 종료한다.
- session rotation·무효화 뒤에는 CSRF bootstrap → session 조회 → route 결정 → 필요한 STOMP 연결 순서로 재수렴한다.

## FE Consumption Notes

- session provider가 bootstrap과 route guard 순서를 소유한다.
- 공통 transport가 credential, CSRF header, 오류 mapping을 담당한다.
- FE 해석: 예상 인증/계정 오류는 route error boundary가 아닌 상태와 다음 행동으로 표시한다.

## Excluded From FE Projection

- cookie 보안 속성, Origin 검증의 서버 내부 처리, session 저장·폐기 구현과 observability 세부.
