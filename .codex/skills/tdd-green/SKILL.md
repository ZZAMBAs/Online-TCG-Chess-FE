---
name: tdd-green
description: Online-TCG-Chess-FE의 로컬 feature 이슈 문서의 TDD RED 결과와 실패 테스트를 기준으로 FE production 최소 구현을 작성해 TDD GREEN 단계를 수행해야 할 때 사용한다. 인자로 auth-1, auth-001, auth-issues-1, xxx-yyy-1처럼 마지막 토큰이 숫자인 이슈 식별자를 받아 이슈, 선행 이슈, RED 결과, 아키텍처 문서를 확인하고, src의 UI/API client/state/STOMP client 구현 및 필요한 테스트 보정만 최소 수정한다. package.json, 테스트 하네스, CI 설정, 광범위 리팩터링, E2E/Playwright는 다루지 않는다.
---

# TDD GREEN

## 개요

로컬 이슈의 RED 테스트를 통과시키기 위한 최소 FE production 구현을 작성한다. GREEN 단계에서는 실패 테스트를 초록색으로 바꾸는 데 필요한 코드만 만들고, 리팩터링, 하네스 도입, 아키텍처 재결정, E2E 테스트 도입은 하지 않는다.

## 입력 규칙

- 모든 질문, 분석, 보고는 한국어로 작성한다.
- 사용자는 이슈 식별자 하나를 인자로 제공해야 한다.
- 인자가 없거나 마지막 하이픈 뒤 토큰이 숫자가 아니면 형식 오류를 보고하고 즉시 종료한다.
- 허용 예시는 `auth-1`, `auth-001`, `auth-issues-1`, `xxx-yyy-1`이다.
- 끝에서 두 번째 토큰이 `issues`이면 구분자로만 보고 feature 이름에서 제외한다.
- `xxx-yyy-1`은 feature=`xxx-yyy`, issue number=`1`로 해석한다.
- 이슈 번호 입력은 0-padding 없이 받아들이되, 이슈 파일 탐색은 번호의 정수값으로 비교한다.
- 이슈 디렉터리는 `docs/features/{feature}/issues/{feature}-{nnn}-{slug}/` 계열에서 정확히 하나만 찾아야 하며, 그 안의 `issue.md`를 이슈 문서로 본다.
- 이슈 탐색은 먼저 `scripts/find_issue.py`를 실행해 검증한다.

```bash
python3 .codex/skills/tdd-green/scripts/find_issue.py auth-1 --root .
```

## 읽을 문서

다음 순서로 존재하는 문서만 읽는다.

1. `scripts/find_issue.py`가 찾은 로컬 이슈 문서
2. 현재 이슈의 `depends_on`, 직전 번호 이슈, `## 의존 관계`에 적힌 선행 이슈 문서
3. 현재 이슈의 `## TDD RED 결과`
4. RED 결과 상태 의미를 확인하기 위한 `.codex/skills/tdd-red/references/red-result-contract.md`
5. RED 결과에 적힌 테스트 파일과 관련 테스트 코드
6. 이슈 frontmatter 또는 본문에 적힌 PRD/TRD/architecture/storyboard/traceability/contract 문서
7. `docs/architecture/*`와 현재 `src`, 테스트 구현 패턴
8. BE 요구사항과 REST/STOMP 계약 확인이 필요한 경우 프로젝트 로컬 `$spec-read` 결과와 `docs/contracts/*`
9. `TDD GREEN 결과`를 기록하기 위한 `references/green-result-contract.md`

PRD/TRD, RED 결과, 테스트 파일, 아키텍처 문서, 구현 대상 컴포넌트·store·API client·STOMP client를 확인할 수 없으면 추측하지 말고 사용자에게 확인을 요청한다. 아키텍처 문서가 없거나 미확정이면 production 구현을 작성하지 않는다.

## 진입 게이트

- 선행 이슈가 있으면 해당 이슈의 AC 충족과 테스트 통과가 문서상 확인되는지 확인한다.
- 선행 이슈 완료 여부가 확인되지 않으면 구현하지 말고 `blocked`로 보고한다.
- 현재 이슈에 `TDD RED 결과`가 없으면 구현하지 말고 `blocked`로 보고한다.
- RED 결과가 모두 `already-green`이면 테스트를 재실행해 확인하고 production 변경 없이 `green-pass`로 보고한다.
- RED 결과가 `blocked`만 있으면 구현하지 말고 해당 차단 사유를 보고한다.
- RED 결과가 `compile-blocked`이면 architecture 문서와 이슈 구현 메모를 기준으로 필요한 production skeleton과 최소 구현을 만들 수 있다.
- RED 결과가 `red-fail`이면 해당 테스트를 통과시키는 최소 구현만 작성한다.

## 변경 허용 범위

- `src` 아래 FE production 코드 생성 또는 수정
- feature 구현에 꼭 필요한 production resource, fixture, schema, static asset 수정
- RED 테스트가 AC와 다르게 작성되었거나 단순 오탈자/import/fixture 오류가 있을 때의 테스트 또는 test resource 보정
- 현재 이슈 문서의 `## TDD GREEN 결과` 섹션 생성 또는 최신 스냅샷 갱신

다음은 GREEN 단계에서 금지한다.

- `package.json`, lockfile, Vite/Vitest/TypeScript/ESLint/CI 설정 수정
- Testing Library, MSW, Vitest, Playwright 같은 하네스 또는 의존성 도입
- E2E/Playwright 테스트 작성, 실행 요구, 설정 변경
- architecture 문서에 없는 라우팅, 상태 관리, API client, STOMP client 구조를 임의로 확정
- RED 테스트와 현재 이슈 AC를 넘는 기능 구현
- BLUE 단계로 넘길 수 있는 구조 개선, 성능 개선, 이름 변경, 대규모 리팩터링
- 무관한 테스트 수정이나 기존 사용자 변경 되돌리기

이미 하네스가 존재하면 실행하거나 통과하도록 구현할 수 있다. 하네스가 없으면 설치하지 말고 `blocked`로 보고하고 `실패 또는 차단 요약`에 하네스 부재를 기록한다.

## 구현 규칙

- architecture 문서가 있으면 routing, page/component 경계, state ownership, API/STOMP adapter 배치, 스타일링 경계를 따른다.
- architecture 문서가 없거나 미확정이면 구현하지 말고 `blocked`로 보고한다.
- architecture 문서와 현재 코드가 충돌하면 구현하지 말고 drift를 보고한다.
- production skeleton이 필요하면 테스트가 요구하는 public surface만 만든다.
- 메서드와 컴포넌트 동작은 테스트 통과에 필요한 가장 작은 동작으로 제한한다.
- 오류, loading, empty, disabled, 권한, REST/STOMP 메시지 포맷은 AC와 RED 테스트가 요구하는 만큼만 구현한다.
- BE 계약과 충돌하면 FE 로컬 테스트에 억지로 맞추지 말고 `$spec-read` 및 계약 문서 기준으로 `test-invalid` 또는 `blocked`를 보고한다.
- RED 테스트가 잘못된 요구를 검증한다고 판단되면 production을 억지로 맞추지 말고 `test-invalid`로 보고하고 사용자 확인을 요청한다.

## GREEN 절차

각 RED 테스트마다 아래 순서를 반복한다.

1. RED 결과에 적힌 테스트를 단독 실행해 현재 실패 상태를 확인한다.
2. 실패 원인을 `compile-blocked`, `red-fail`, `test-invalid`, `blocked`, `green-failed`로 분류한다.
3. `compile-blocked`이면 architecture 기준으로 필요한 production component, module, export, route, store, API client를 최소 생성한다.
4. `red-fail`이면 테스트를 통과시키는 최소 production 구현만 작성한다.
5. 테스트 코드 자체의 오탈자, import, fixture 오류이면 AC를 보존하는 범위에서 테스트를 보정한다.
6. 같은 테스트를 다시 실행해 통과 여부를 확인한다.
7. 통과하면 다음 RED 테스트로 넘어간다.

모든 대상 테스트가 통과하면 가능한 범위에서 전체 unit/component 테스트와 typecheck를 실행한다. 실패가 남으면 이번 이슈 관련 실패, 기존 실패, 환경 실패, 하네스 부재를 구분한다.

## GREEN 결과 기록

현재 이슈 문서에 `## TDD GREEN 결과` 섹션을 만들거나 갱신한다. `references/green-result-contract.md`를 읽고, 그 계약의 항목과 상태 의미를 따른다. 실행 이력을 누적하지 말고 현재 GREEN 단계의 최신 스냅샷만 남긴다.

## 실행 명령

테스트 실행은 현재 FE 프로젝트의 `package.json`과 설정 파일에 맞춰 수행한다. 명령이 없으면 추측해 설치하지 말고 `blocked`로 기록한다.

```bash
npm test -- --run path/to/file.spec.ts
npm run test -- --run path/to/file.spec.ts
npm run test:unit -- path/to/file.spec.ts
npm run typecheck
```

테스트 실행이 환경 문제로 실패하면 원인을 분리해 보고한다. 네트워크, 권한, 포트, 브라우저 설치 같은 외부 원인 때문에 검증할 수 없으면 구현 파일 작성 결과와 미검증 항목을 명확히 남긴다.

## 완료 보고

작업을 마치면 다음만 간결히 보고한다.

- 사용한 이슈 문서
- 읽은 `TDD RED 결과`
- 생성 또는 수정한 production 파일
- 보정한 테스트 또는 resource 파일
- 갱신한 `TDD GREEN 결과`
- 각 테스트의 상태: `green-pass`, `test-invalid`, `blocked`, `green-failed`
- 전체 unit/component 테스트와 typecheck 실행 결과
- BLUE 단계로 넘길 리팩터링 후보나 하네스 이슈가 있으면 그 이유
