---
name: tdd-blue
description: Online-TCG-Chess-FE의 로컬 feature 또는 foundation 이슈의 GREEN 결과와 production 변경을 기준으로 BLUE 리팩터링을 수행해야 할 때 사용한다. 새 기능·테스트 수정 없이 GREEN 범위에서 컴포넌트, style/token/primitive, state, API/STOMP 경계와 중복·네이밍을 최소 정리하며 E2E는 다루지 않는다.
---

# TDD BLUE

## 개요

GREEN으로 통과한 FE production 구현을 기능 변화 없이 정리한다. BLUE 단계는 새 기능을 만들거나 테스트를 고치지 않고, 리팩터링 전후 unit/component 테스트와 typecheck가 통과하는 범위에서 구조, 중복, 이름, 컨벤션을 개선한다.

## 입력 규칙

- 모든 질문, 분석, 보고는 한국어로 작성한다.
- 사용자는 이슈 식별자 하나를 인자로 제공해야 한다.
- 인자가 없거나 마지막 하이픈 뒤 토큰이 숫자가 아니면 형식 오류를 보고하고 즉시 종료한다.
- 허용 예시는 `auth-1`, `auth-001`, `auth-issues-1`, `xxx-yyy-1`이다.
- 끝에서 두 번째 토큰이 `issues`이면 구분자로만 보고 feature 이름에서 제외한다.
- `xxx-yyy-1`은 feature=`xxx-yyy`, issue number=`1`로 해석한다.
- 이슈 번호 입력은 0-padding 없이 받아들이되, 이슈 디렉터리 탐색은 번호의 정수값으로 비교한다.
- 이슈 디렉터리는 `docs/features/{feature}/issues/{feature}-{nnn}-{slug}/` 계열에서 정확히 하나만 찾아야 하며, 그 안의 `issue.md`를 이슈 문서로 본다.
- 이슈 탐색은 먼저 `scripts/find_issue.py`를 실행해 검증한다.

```bash
python3 .codex/skills/tdd-blue/scripts/find_issue.py auth-1 --root .
```

## 읽을 문서

다음 순서로 존재하는 문서만 읽는다.

1. `scripts/find_issue.py`가 찾은 `issue.md`
2. 현재 이슈의 `depends_on`, 직전 번호 이슈, `## 의존 관계`에 적힌 선행 이슈 문서
3. 현재 이슈의 `## TDD RED 결과`와 `## TDD GREEN 결과`
4. GREEN 결과 상태 의미를 확인하기 위한 `.codex/skills/tdd-green/references/green-result-contract.md`
5. 이슈 frontmatter 또는 본문에 적힌 PRD/TRD/architecture/storyboard/traceability/contract 문서
6. `docs/architecture/*`와 현재 `src`, 테스트 구현 패턴
7. 리팩터링 체크리스트인 `references/refactor-checklist.md`
8. 로그 기록 계약인 `references/refactor-log-contract.md`

PRD/TRD, GREEN 결과, 아키텍처 문서, 리팩터링 대상 파일을 확인할 수 없으면 추측하지 말고 `blue-blocked`로 기록한다.

`slice_type: foundation`은 feature PRD 대신 issue가 참조하는 approved root TRD, fixed architecture, 관련 디자인 기준을 근거로 사용한다.

## 진입 게이트

- 선행 이슈가 있으면 해당 이슈의 AC 충족, 테스트 통과, BLUE 완료 또는 BLUE 불필요가 문서상 확인되는지 확인한다.
- 현재 이슈에 `TDD GREEN 결과`가 없으면 리팩터링하지 말고 `blue-blocked`로 기록한다.
- GREEN 결과가 `green-pass`가 아니면 리팩터링하지 말고 `blue-blocked`로 기록한다.
- GREEN 결과의 production 파일 목록을 우선 리팩터링 대상으로 삼는다.
- GREEN 결과만으로 대상 파일을 특정할 수 없으면 `git diff --name-only`에서 현재 이슈와 관련된 `src` production/resource 변경만 후보로 삼는다.
- 대상 파일을 특정할 수 없으면 리팩터링하지 말고 `blue-blocked`로 기록한다.
- 리팩터링 전 대상 테스트와 가능한 전체 unit/component 테스트, typecheck를 실행해 baseline green을 확인한다.
- baseline이 green이 아니면 리팩터링하지 말고 `blue-blocked`로 기록한다.

## 변경 허용 범위

- GREEN 변경 범위 안의 `src` production 코드
- GREEN 변경 범위 안에서 리팩터링에 꼭 필요한 production resource
- 현재 이슈 디렉터리의 `refactor-log.md`

다음은 BLUE 단계에서 금지한다.

- 새 기능 추가
- 테스트 코드 수정
- `package.json`, lockfile, Vite/Vitest/TypeScript/ESLint/CI 설정 수정
- Testing Library, MSW, Vitest, Playwright 같은 하네스 또는 의존성 도입
- E2E/Playwright 테스트 작성, 실행 요구, 설정 변경
- GREEN 변경 범위를 벗어난 광범위 리팩터링
- 아키텍처 문서에 없는 routing, state ownership, API/STOMP adapter 경계를 새로 확정
- 리팩터링할 부분이 없는데 의도적으로 수정

## 리팩터링 규칙

- `references/refactor-checklist.md`를 기준으로 컴포넌트 책임, state ownership, API/STOMP adapter 경계, 중복, 네이밍, 컨벤션, 오버엔지니어링을 점검한다.
- foundation 변경에서는 token 중복, primitive variant 책임, 전역 style 누수와 후속 feature가 우회할 수 있는 비공개 경계를 함께 점검한다.
- 테스트를 더 쉽게 통과시키기 위한 동작 변경은 하지 않는다.
- public component props/events, route contract, REST/STOMP payload, 오류 포맷, 사용자 표시 문구의 의미는 기존 AC와 GREEN 테스트가 보장하는 동작을 유지한다.
- 구조 개선은 GREEN 변경을 이해하기 쉽게 만드는 최소 수준으로 제한한다.
- 중복 제거가 오히려 추상화를 과하게 만들면 그대로 둔다.
- 리팩터링 후보가 없으면 파일을 수정하지 말고 `blue-noop`로 기록한다.

## BLUE 절차

1. `scripts/find_issue.py`로 이슈 디렉터리와 `issue.md`를 찾는다.
2. RED/GREEN 결과, 아키텍처 문서, GREEN 변경 파일을 확인한다.
3. 대상 테스트와 가능한 전체 unit/component 테스트, typecheck를 실행해 baseline green을 확인한다.
4. `references/refactor-checklist.md`로 리팩터링 필요 여부를 판단한다.
5. 리팩터링 후보가 없으면 `refactor-log.md`를 `blue-noop` 최신 스냅샷으로 갱신하고 종료한다.
6. 후보가 있으면 한 번에 작은 리팩터링만 적용한다.
7. 대상 테스트와 가능한 전체 unit/component 테스트, typecheck를 다시 실행한다.
8. 실패하면 해당 시도 변경만 되돌리고 원인을 재판단한다.
9. 리팩터링 시도는 최대 3회까지만 한다.
10. 3회 실패하면 `refactor-log.md`에 실패 시도 내역을 누적 기록하고 종료한다.
11. 성공하면 `refactor-log.md`를 `blue-pass` 최신 스냅샷으로 덮어쓴다.

## 로그 기록

현재 이슈 디렉터리의 `refactor-log.md`를 만들거나 갱신한다. `references/refactor-log-contract.md`를 읽고 그 계약의 항목과 상태 의미를 따른다.

- `blue-pass`, `blue-noop`, `blue-blocked`는 실행 이력을 누적하지 말고 최신 스냅샷만 남긴다.
- `blue-failed`는 3회 실패 시도 내역을 누적 가능하게 기록한다.
- 일반 회귀 테스트 재실행 로그는 BLUE 실행의 일부일 때만 요약에 반영한다.

## 실행 명령

테스트 실행은 현재 FE 프로젝트의 `package.json`과 설정 파일에 맞춰 수행한다. 명령이 없으면 추측해 설치하지 말고 `blue-blocked`로 기록한다.

```bash
npm test -- --run path/to/file.spec.ts
npm run test -- --run path/to/file.spec.ts
npm run test:unit -- path/to/file.spec.ts
npm run typecheck
```

테스트 실행이 환경 문제로 실패하면 원인을 분리해 `blue-blocked` 또는 실패 시도 사유로 기록한다.

## 완료 보고

작업을 마치면 다음만 간결히 보고한다.

- 사용한 이슈 문서
- 리팩터링 대상 파일
- 변경한 production 파일
- `refactor-log.md` 갱신 상태: `blue-pass`, `blue-noop`, `blue-blocked`, `blue-failed`
- baseline 및 회귀 테스트 실행 결과
- rollback 여부와 실패 시도 횟수
- 남은 리팩터링 후보가 있으면 BLUE에서 제외한 이유
