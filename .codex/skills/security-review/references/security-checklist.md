# Security Checklist

현재 이슈의 FE 변경 범위와 관련 있는 항목만 검토한다. 요구사항의 원천은 프로젝트 로컬 `$spec-read`, `docs/contracts/*`, 기능 PRD/TRD, architecture 문서, 이슈 AC다.

## 인증과 세션

- 서버 세션과 쿠키 기준 인증 전제를 FE에서 깨지 않는다.
- JWT Access/Refresh Token을 MVP 기본 인증으로 임의 도입하지 않는다.
- 비밀번호, 세션 식별자, 이메일 인증 토큰, 비밀번호 재설정 토큰, 민감 응답값을 console, 화면, URL, localStorage/sessionStorage에 노출하지 않는다.
- 인증 전 사용자와 미완료 계정은 허용된 최소 화면과 action만 접근할 수 있게 route guard와 UI 상태를 맞춘다.
- 로그아웃, 세션 만료, 인증 실패 후 캐시된 민감 화면이나 상태가 남지 않게 한다.

## 인가와 소유권

- 사용자 입력의 `userId`, `senderId`, 닉네임, 권한 값을 신뢰해 FE에서 권한을 확정하지 않는다.
- 관리자, 신고, 덱, 컬렉션, 경기, 기보, 게시글 원문 접근은 서버 응답과 계약을 기준으로 표시한다.
- UI 숨김을 보안 통제로 착각하지 않는다. 버튼 숨김은 사용자 경험이고, 최종 권한은 서버가 검증해야 한다.
- 타 사용자 데이터가 route param, store cache, optimistic update, STOMP payload 조합으로 섞이지 않는지 확인한다.

## REST와 오류 응답

- API client는 credentials/cookie 정책을 architecture와 BE 계약에 맞춘다.
- 오류 메시지에 내부 구현, stack trace, SQL, 보안 정책 세부, 토큰 값을 그대로 표시하지 않는다.
- 입력 검증 실패 후 낙관적 UI 상태가 실제 서버 상태처럼 남지 않게 rollback 또는 재조회 경로를 둔다.
- CSRF, CORS, SameSite 쿠키 전제를 FE 코드가 임의 변경하거나 우회하지 않는다.
- rate limit이 요구된 흐름에서 FE가 자동 재시도나 병렬 요청으로 제한을 우회하도록 만들지 않는다.

## STOMP와 실시간 경기

- STOMP destination, subscription, send payload를 클라이언트 권위로 취급하지 않는다.
- 개인 채널 라우팅이나 사용자 식별은 서버 계약과 인증 세션 전제를 따른다.
- 클라이언트가 보낸 게임 상태, 카드 효과, 턴, 타이머, 승패, 보상, 권한 값은 UI 표시 입력일 뿐 서버 권위 상태로 확정하지 않는다.
- 거부된 명령, 인증 실패, 연결 끊김 후 UI 상태가 성공처럼 남지 않게 한다.
- 과도한 SEND, 중복 클릭, reconnect 루프가 서버 부담이나 중복 명령을 만들지 않게 한다.

## 브라우저와 렌더링

- 사용자 생성 콘텐츠, 게시글, 채팅, 닉네임, 신고 원문은 안전하게 escape/sanitize한다.
- `v-html`, `innerHTML`, markdown/html 렌더링, URL 링크 처리에 XSS 위험이 없는지 확인한다.
- 외부 링크는 필요 시 `rel="noopener noreferrer"`를 적용한다.
- 파일 업로드, 이미지 URL, 외부 리소스는 MVP 범위와 보안 계약을 벗어나 임의 도입하지 않는다.

## 저장과 캐시

- 민감 데이터는 localStorage/sessionStorage/IndexedDB에 저장하지 않는다.
- store cache는 로그아웃, 계정 전환, 권한 변경, 제재 상태 변경 시 정리된다.
- optimistic update는 서버 실패, 권한 거부, STOMP 정정 이벤트에서 되돌릴 수 있어야 한다.

## 도구와 검증

- unit/component 테스트, typecheck, lint, audit 결과를 확인한다.
- Playwright 또는 E2E 결과가 이미 있으면 보안 finding 재현과 회귀 근거로 사용할 수 있다.
- 새 보안 도구나 Playwright 설정 도입은 사용자 승인 또는 별도 이슈로 분리한다.
