---
name: e2e-test
description: Online-TCG-Chess-FE에서 로컬 feature 또는 foundation 이슈의 UI/화면 흐름을 기존 Playwright 설정으로 브라우저 E2E와 대표 시각 상태로 검증해야 할 때 사용한다. issue의 e2e_required와 visual_states를 기준으로 desktop/mobile, 오류·권한·실시간 상태를 검증하고 e2e-test.md에 결과를 기록하며, 캡처는 검증 후 삭제하고 Playwright·package·CI 설정은 수정하지 않는다.
---

# E2E Test

## 역할

- `$e2e-test`는 TDD GREEN/BLUE 이후의 실제 브라우저 검증을 담당한다.
- 모든 이슈에 실행하지 않는다. issue frontmatter의 `e2e_required: true` 또는 본문의 E2E 요구가 있을 때만 실행한다.
- 사용자 흐름, desktop/mobile 정보 우선순위, 대표 오류·권한·실시간 상태를 기존 Playwright 환경으로 검증한다.
- pixel-perfect 비교는 fixed architecture가 별도로 승인한 경우에만 수행한다. 기본은 design baseline과 storyboard의 의미·상태·접근성에 대한 visual smoke다.

## 시작 절차

1. `scripts/find_issue.py`로 대상 `issue.md`를 찾는다.
2. `e2e_required`, `visual_states`, `## Acceptance Criteria`, `## 테스트`, `## 구현 메모`를 읽는다.
3. `references/e2e-result-contract.md`를 읽는다.
4. 이슈가 참조하는 approved `docs/design/design-baseline.md`, storyboard, TRD, fixed architecture, GREEN/BLUE 결과를 읽는다.
5. 기존 `playwright.config.*`, package scripts, 관련 E2E 테스트와 fixture를 확인한다.
6. `e2e_required`가 아니면 production/test 파일을 만들지 않고 `e2e-not-required` 결과를 기록한다.

## 진입 게이트

- `e2e_required: true`이면 GREEN 결과가 `green-pass`이고 BLUE 결과가 `blue-pass` 또는 `blue-noop`여야 한다.
- approved design baseline, fixed architecture, 관련 storyboard/visual state 근거가 없으면 `e2e-blocked`로 기록한다.
- Playwright 설정, 브라우저, 실행 명령, 필요한 인증/fixture 경로가 없으면 설치하거나 설정을 바꾸지 말고 `e2e-blocked`로 기록한다.
- 새 Playwright, package, CI, fixture architecture 도입은 `$architecture-decision` 또는 사용자 승인 대상이다.

## 변경 허용 범위

- 기존 Playwright 설정이 인식하는 대상 이슈 전용 새 E2E test file과 test resource
- 현재 이슈 디렉터리의 `e2e-test.md`

다음은 수정하지 않는다.

- 기존 E2E/unit/component 테스트 파일
- 앱 source, fixture architecture, Playwright/package/CI 설정
- 요구사항, PRD, TRD, architecture, design baseline, storyboard

## 검증 범위

- issue AC가 요구하는 사용자 시작점, 행동, 완료 결과
- desktop과 mobile viewport의 정보 우선순위와 핵심 CTA
- issue의 `visual_states`에 기록된 오류, 권한 거부, loading/empty, 대기, 재접속 같은 대표 상태
- semantic role/name, keyboard/focus, visible feedback, route 전환
- design baseline의 component variant와 responsive/a11y 기준

다음은 기본 범위에서 제외한다.

- 모든 화면·모든 상태의 screenshot snapshot
- 디자인 기준에 없는 pixel-perfect 수치 비교
- API/STOMP 계약 또는 production UI 구현 변경
- Playwright 설정, package, CI, 브라우저 설치 변경

## 캡처 정책

- screenshot, trace, video는 검증 중 임시 근거로만 사용한다.
- 결과를 확인한 뒤 기본적으로 삭제하고, `e2e-test.md`에는 viewport, 상태, 통과/실패 요약만 남긴다.
- 실패 캡처도 사용자가 보관을 요청하지 않으면 삭제한다.
- fixed architecture가 visual regression baseline 보존을 승인한 경우에만 해당 baseline과 실패 artifact 정책을 따른다.

## 결과 기록

현재 이슈 디렉터리의 `e2e-test.md`를 최신 스냅샷으로 생성 또는 갱신한다.

- `e2e-pass`: 요구된 흐름과 대표 상태가 통과
- `e2e-failed`: 테스트 또는 시각/상태 검증 실패
- `e2e-blocked`: 하네스, 기준 문서, 환경 또는 fixture가 없어 실행 불가
- `e2e-not-required`: 이슈가 E2E 대상이 아님

## 후속 handoff

- `$security-review`: `e2e-test.md`를 보안 재현과 UI 권한/오류 검토 근거로 읽는다.
- AC verifier: `e2e_required: true`인 이슈는 `e2e-pass`가 아니면 AC 전체 통과로 판정하지 않는다.
- `$tdd-workflow`: UI/대표 상태 이슈에서는 BLUE 뒤 E2E를 실행하고, E2E 통과 후 security-review와 AC verifier로 진행한다.

## 금지 사항

- 앱 소스, 테스트 하네스, package, Playwright 설정, CI를 수정하지 않는다.
- 디자인 기준 없이 시각적 결함을 임의 기준으로 판정하지 않는다.
- 캡처·trace·video를 장기 산출물로 남기지 않는다.
