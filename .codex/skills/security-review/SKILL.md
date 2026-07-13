---
name: security-review
description: Online-TCG-Chess-FE에서 TDD BLUE 이후 또는 별도 e2e-test 이후 로컬 feature/foundation 이슈의 FE production 변경을 독립 보안 검증해야 할 때 사용한다. UI/style/primitive/API/STOMP/state 변경과 관련 문서·diff를 검토하고 Medium 이상을 차단하며 security-review.md에 최신 결과를 기록한다.
---

# Security Review

## 개요

TDD BLUE 또는 별도 e2e-test 이후 FE production 변경을 독립 검증한다. 이 스킬은 FE에서 생길 수 있는 보안 결함을 찾고, `Medium` 이상 finding을 수정 게이트로 삼고, 검토 결과를 이슈 디렉터리의 `security-review.md`에 남긴다.

## 입력 규칙

- 모든 질문, 분석, 보고는 한국어로 작성한다.
- 사용자는 이슈 식별자 하나를 인자로 제공해야 한다.
- 인자가 없거나 마지막 하이픈 뒤 토큰이 숫자가 아니면 형식 오류를 보고하고 즉시 종료한다.
- 허용 예시는 `auth-1`, `auth-001`, `auth-issues-1`, `xxx-yyy-1`이다.
- 끝에서 두 번째 토큰이 `issues`이면 구분자로만 보고 feature 이름에서 제외한다.
- 이슈 디렉터리는 `docs/features/{feature}/issues/{feature}-{nnn}-{slug}/` 계열에서 정확히 하나만 찾아야 하며, 그 안의 `issue.md`를 이슈 문서로 본다.
- 이슈 탐색은 먼저 `scripts/find_issue.py`를 실행해 검증한다.

```bash
python3 .codex/skills/security-review/scripts/find_issue.py auth-1 --root .
```

## 읽을 문서

다음 순서로 존재하는 문서만 읽는다.

1. `scripts/find_issue.py`가 찾은 `issue.md`
2. 현재 이슈의 `depends_on`, 직전 번호 이슈, `## 의존 관계`에 적힌 선행 이슈 문서
3. 현재 이슈의 `## TDD RED 결과`와 `## TDD GREEN 결과`
4. 현재 이슈 디렉터리의 `refactor-log.md`
5. 현재 이슈 디렉터리의 e2e-test 결과 문서가 있으면 해당 문서
6. 이슈 frontmatter 또는 본문에 적힌 PRD/TRD/architecture/storyboard/traceability/contract 문서
7. 보안 원천 요구사항 확인을 위한 프로젝트 로컬 `$spec-read` 결과와 `docs/contracts/*`
8. 현재 `src`, 테스트, `package.json`, 설정 파일, HTTP/STOMP/auth/router/store 관련 구현
9. 이번 이슈 변경 범위 확인을 위한 `git diff --name-only`, `git diff`, 필요 시 `git diff --cached`
10. 보안 체크리스트인 `references/security-checklist.md`
11. 도구 사용 정책인 `references/tooling-policy.md`
12. 로그 기록 계약인 `references/security-review-contract.md`

PRD/TRD, GREEN 결과, BLUE 결과, 변경 파일, 보안 요구사항을 확인할 수 없으면 추측하지 말고 `security-blocked`로 기록한다. 단, 사용자가 명시적으로 e2e-test 이후 보안 검토를 요청한 경우에는 e2e-test 산출물을 추가 근거로 읽되, TDD 산출물이 없으면 누락 영향을 기록한다.

`slice_type: foundation`은 feature PRD 대신 issue가 참조하는 root TRD, fixed architecture, 관련 디자인 기준을 사용하고 공통 UI primitive의 안전한 렌더링·focus 처리·전역 style 경계를 검토한다.

## 진입 게이트

- 현재 이슈에 `TDD GREEN 결과`가 없으면 기본적으로 검토하지 말고 `security-blocked`로 기록한다.
- GREEN 결과가 `green-pass`가 아니면 검토하지 말고 `security-blocked`로 기록한다.
- `refactor-log.md`가 없거나 BLUE 상태가 `blue-pass` 또는 `blue-noop`가 아니면 기본적으로 검토하지 말고 `security-blocked`로 기록한다.
- `e2e_required: true`인데 `e2e-test.md`가 없거나 결과가 `e2e-pass`가 아니면 검토하지 말고 `security-blocked`로 기록한다.
- 사용자가 e2e-test 이후 보안 검토를 요청했고 e2e-test 산출물이 명확하면, BLUE 누락 여부를 별도 갭으로 기록하고 보안 검토를 제한적으로 진행할 수 있다.
- 대상 파일은 GREEN 결과의 production 파일, BLUE 변경 파일, e2e-test 관련 파일, 현재 `git diff` 중 이슈 관련 production/resource 파일로 제한한다.
- 대상 파일을 특정할 수 없으면 `security-blocked`로 기록한다.
- 선행 이슈가 있으면 해당 이슈의 AC 충족, 테스트 통과, BLUE 완료 또는 BLUE 불필요가 문서상 확인되는지 확인한다.

## 변경 허용 범위

기본 검토 단계에서는 파일을 수정하지 않는다. finding 수정이 필요하면 메인 에이전트만 아래 범위에서 수정할 수 있다.

- 현재 이슈의 GREEN/BLUE 변경 범위 안의 `src` production 코드
- 현재 이슈의 GREEN/BLUE 변경 범위 안에서 보안 결함 수정에 꼭 필요한 production resource
- 현재 이슈 디렉터리의 `security-review.md`
- 사용자가 승인한 경우의 보안 도구, Playwright, package, CI 설정

다음은 기본 보안 검토에서 금지한다.

- 새 기능 추가
- 보안 결함 은폐 목적의 테스트 수정
- 이슈 범위를 벗어난 광범위 보안 리팩터링
- 사용자 승인 없는 새 보안 도구, Playwright, 의존성, CI 설정 도입
- 아키텍처 문서에 없는 인증/인가 구조 재결정
- `Low` finding만 있는 상태에서 불필요한 production 수정

## 보안 검토 절차

1. `scripts/find_issue.py`로 이슈 디렉터리와 `issue.md`를 찾는다.
2. GREEN/BLUE 결과, e2e-test 산출물, 변경 파일을 확인한다.
3. `references/security-checklist.md`와 `$spec-read`/`docs/contracts/*`에서 이번 이슈에 적용되는 보안 요구사항을 추린다.
4. `references/tooling-policy.md`에 따라 기존 unit/component 테스트, typecheck, lint, audit, 이미 존재하는 보안 도구를 실행한다.
5. Playwright가 이미 구성되어 있거나 e2e-test 스킬 산출물이 있으면, 보안 finding 재현이나 회귀 확인에 필요한 범위에서 Playwright 테스트를 실행할 수 있다.
6. 필요한 새 보안 도구나 Playwright 설정이 있으면 즉시 도입하지 말고 후보, 이유, 예상 변경 범위를 기록한다. 사용자가 승인한 경우에만 설정을 변경한다.
7. 변경 파일을 독립 관점으로 다시 읽어 보안 finding을 분류한다.
8. `Medium` 또는 `High` finding이 있으면 허용 범위 안에서 수정하고 관련 테스트를 재실행한다.
9. 수정 후 같은 범위로 보안 검토를 다시 수행한다.
10. `security-review.md`를 최신 스냅샷으로 갱신한다.

## 심각도 기준

- `High`: 토큰/세션/비밀번호/이메일 인증값 노출, 클라이언트 조작으로 타 사용자 데이터 접근 가능, STOMP destination/게임 상태 조작을 신뢰, 관리자 기능 우회, XSS로 즉시 악용 가능한 렌더링, 민감 정보 localStorage 저장처럼 즉시 악용 가능한 결함
- `Medium`: 특정 조건에서 권한/소유권 UI가 서버 계약과 충돌하거나, 오류 정보 노출, CSRF/CORS/쿠키 전제 오해, rate limit 회피를 유도하는 클라이언트 로직, 보안 로그/감사 요구 누락을 숨기는 UI 흐름
- `Low`: 직접 악용 가능성은 낮지만 방어적 입력 검증, 메시지 품질, 보안 관측성, 민감값 마스킹, 설정 명확성을 개선할 수 있는 항목

`Medium` 이상은 차단한다. `Low`만 있으면 production을 수정하지 않고 `security-low-only`로 완료할 수 있다.

## 실행 명령

테스트 실행은 현재 FE 프로젝트의 `package.json`과 설정 파일에 맞춰 수행한다.

```bash
npm test -- --run path/to/file.spec.ts
npm run test -- --run path/to/file.spec.ts
npm run test:unit -- path/to/file.spec.ts
npm run typecheck
npm run lint
npm audit
npx playwright test path/to/file.spec.ts
```

Playwright 명령은 이미 구성되어 있거나 e2e-test 산출물 검증에 필요한 경우에만 실행한다. 새 도구 실행이 네트워크, 권한, 설치 문제로 막히면 원인을 분리해 `security-blocked` 또는 도구 후보로 기록한다.

## 로그 기록

현재 이슈 디렉터리의 `security-review.md`를 만들거나 갱신한다. `references/security-review-contract.md`를 읽고 그 계약의 항목과 상태 의미를 따른다.

- `security-pass`, `security-low-only`, `security-blocked`, `security-failed`는 실행 이력을 누적하지 말고 최신 스냅샷만 남긴다.
- `Medium` 이상 finding이 수정되어 재검증까지 통과하면 최종 상태는 `security-pass`로 기록하고, 수정된 finding과 재검증 결과를 남긴다.
- `Medium` 이상 finding이 남아 있으면 `security-failed`로 기록한다.

## 완료 보고

작업을 마치면 다음만 간결히 보고한다.

- 사용한 이슈 문서
- 검토 대상 production/resource/e2e 관련 파일
- 발견한 `Low`/`Medium`/`High` 항목 수
- `Medium`/`High` 수정 파일과 재검증 결과
- `security-review.md` 갱신 상태: `security-pass`, `security-low-only`, `security-blocked`, `security-failed`
- 실행한 테스트와 보안/정적 분석 명령
- 새 보안 도구 또는 Playwright 설정 도입 후보가 있으면 사용자 승인 필요 여부
