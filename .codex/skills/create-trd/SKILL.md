---
name: create-trd
description: Online-TCG-Chess-FE에서 .cache/prd-read/docs의 BE PRD와 필요 시 BE 요구사항 원천, 확정된 FE architecture, storyboard, fixed FE/BE contract projection을 기준으로 전체 FE TRD hub와 기능별 TRD를 한국어로 생성·갱신해야 할 때 사용한다. $architecture-decision 이후 docs/architecture/current-fixed.md의 fixed 결정을 따르고, docs/trd.md와 docs/features/{feature}/trd.md를 작성하며, 승인된 범위에서 package.json 등 build/harness 설정을 보정할 수 있지만 issue/ADR/TDD 구현, PRD 원문 수정, BE 계약 임의 확정, milestones/websocket-spec 임의 생성은 하지 않는다.
---

# Create TRD

## 개요

확정된 PRD와 FE 아키텍처 결정을 구현 가능한 기술 요구사항으로 번역한다. 이 스킬은 기능별 TRD를 중심으로 작성하고, 루트 `docs/trd.md`는 전체 FE 기술 허브와 추적 색인으로 유지한다.

## 기본 원칙

- 모든 질문, 분석, 문서는 한국어로 작성한다.
- PRD 확인은 `$prd-read`를 사용한다. 원격 최신성 확인 실패 시 캐시 기준으로 추정하지 않는다.
- PRD만으로 요구사항 판단이 부족하거나 REST/STOMP 동작, 권한, 도메인 정책, PRD 충돌을 확인해야 하면 `$spec-read`로 BE 요구사항 원천을 확인한다.
- `$spec-read`가 실패하면 요구사항 원천 기반 TRD 생성을 중단한다.
- FE 아키텍처 기준은 `docs/architecture/current-fixed.md`가 가리키는 fixed 문서다.
- 아키텍처가 확정되지 않았거나 `current-fixed.md` 상태가 `fixed`가 아니면 TRD 생성을 중단하고 `$architecture-decision`을 먼저 요청한다.
- FE 로컬 추정, PRD, BE 요구사항, 아키텍처가 충돌하면 BE 요구사항과 fixed architecture를 우선하고 충돌 항목을 보고한다.
- `docs/spec/*`, `.cache/prd-read/docs/*`의 PRD 원천, storyboard, contract projection, architecture 문서는 입력으로만 취급한다.
- `docs/design/design-baseline.md`가 없거나 `approved`가 아니면 디자인 시스템 소비, 반응형, 접근성, 시각 acceptance를 확정할 수 없으므로 TRD 생성을 중단하고 `$design-decision`을 먼저 요청한다.
- TRD는 기술 요구사항 문서다. feature production 구현 코드, issue 분리, ADR, GitHub Issue, TDD RED/GREEN/BLUE 결과를 작성하지 않는다.
- 단, fixed architecture와 TRD 진입 조건을 만족시키기 위해 필요한 공통 build/harness 설정은 사용자 승인 후 생성하거나 수정할 수 있다. 허용 범위는 `package.json`, lockfile, Vite/Vitest/TypeScript/ESLint/Prettier/Playwright 설정, Git hook `.mjs`, CI 설정, 테스트 하네스 scaffold처럼 기능 구현 전제에 해당하는 공통 설정으로 제한한다.
- `docs/milestones.md`, `docs/websocket-spec.md` 같은 공통 기술 문서는 BE 원천 또는 FE/BE 협의 산출물로 확인한다. FE 추정으로 새로 만들거나 확정하지 않는다.
- 파일 작성 전에는 반영 예정 요약을 세션에 제시하고 승인받는다.

## 대상 범위

사용자가 `{feature}` 인자를 주면 해당 feature만 처리한다. 예를 들어 `$create-trd matchmaking`은 `docs/features/matchmaking/trd.md`만 생성 또는 갱신하고, 필요하면 `docs/trd.md`의 색인을 함께 갱신한다.

인자가 없으면 `$prd-read`로 확인한 feature PRD 목록을 기준으로 전체 feature 후보를 탐색한다. 처리 범위가 넓거나 불명확하면 feature 목록, 기존 TRD 여부, 미확정 의존성을 요약해 사용자에게 처리 순서를 확정받는다.

feature 이름은 PRD 원천 또는 기존 `docs/features/{feature}` 디렉터리명을 그대로 사용한다. 유사 이름을 추측해 진행하지 않는다.

## 먼저 확인할 자료

존재하는 파일만 읽는다.

- `AGENTS.md`
- `.codex/skills/prd-read/SKILL.md`
- `.codex/skills/spec-read/SKILL.md`
- `docs/architecture/current-fixed.md`
- `docs/architecture/fixed-*/impl-fixed.md`
- `docs/architecture/fixed-*/infra-fixed.md`
- `docs/architecture/fixed-*/harness-fixed.md`
- `docs/architecture/*create-trd-handoff*.md`, `docs/architecture/*traceability*.md`
- `docs/contracts/*`
- `docs/design/storyboard.html`, `docs/design/storyboard-pages.md`, `docs/design/storyboard-manifest.json`, `docs/design/storyboard/fragments/*`
- `docs/design/design-baseline.md`, 존재하는 경우의 `docs/design/design-specimen.*`
- 기존 `docs/trd.md`, `docs/features/*/trd.md`
- 참고용 FE 코드와 설정: `package.json`, lockfile, `src`, `app`, `components`, `pages`, `routes`, 테스트/빌드/CI 설정

## 입력 게이트

다음 중 하나라도 실패하면 문서를 쓰지 말고 중단한다.

- `$prd-read`가 PRD 원천 최신성을 확인하지 못한다.
- 대상 feature PRD가 없다.
- `docs/architecture/current-fixed.md`가 없거나 fixed 상태가 아니다.
- `docs/design/design-baseline.md`가 없거나 status가 `approved`가 아니다.
- current fixed 포인터가 가리키는 `impl-fixed.md`, `infra-fixed.md`, `harness-fixed.md` 중 필요한 문서를 읽을 수 없다.
- TRD에 필요한 REST/STOMP 계약이 `docs/contracts/*` 또는 BE fixed 협의 문서로 확인되지 않았다.
- PRD, BE 요구사항 원천, fixed architecture 사이 충돌이 있고 사용자의 재확정 없이 기술 요구사항을 쓸 수 없다.

## 진행 절차

1. `{feature}` 인자 유무를 확인해 대상 범위를 정한다.
2. `$prd-read`로 hub PRD와 대상 feature PRD 최신성을 확인한다.
3. 필요한 경우 `$spec-read`로 BE 요구사항 원천을 확인한다.
4. `docs/architecture/current-fixed.md`를 읽고 active fixed 디렉터리를 따른다.
5. fixed architecture의 구현/인프라/하네스 제약과 create-trd handoff 항목을 추출한다.
6. storyboard, 존재하는 디자인 기준, contract projection에서 대상 feature와 관련된 화면, 상호작용, 디자인 시스템 소비, REST/STOMP 계약 의존성을 추적한다.
7. 기존 `docs/trd.md`와 feature TRD가 있으면 먼저 읽고 중복 생성 대신 갱신한다.
8. feature별 기술 요구사항, 비범위, 라우팅/컴포넌트 책임, 상태 소유권, API/STOMP 요구, 에러/권한/로딩 처리, 디자인 시스템 소비와 시각 acceptance, 테스트 기대, 미확정 의존성을 도출한다.
9. TRD 작성 또는 후속 TDD 진입에 필요한 build/harness 설정 갭이 있으면 fixed architecture와 연결해 반영 후보를 분리한다.
10. `references/trd-template.md`를 읽고 TRD 초안을 작성한다.
11. 파일 작성 전 `docs/trd.md` 갱신 요약, feature TRD별 초안 요약, build/harness 설정 수정 후보를 사용자에게 제시하고 승인받는다.
12. 승인된 문서만 생성 또는 갱신하고, 승인된 build/harness 설정만 수정한다.
13. 설정을 수정한 경우 가능한 범위에서 typecheck/lint/test/build 명령을 실행한다.
14. 완료 시 생성/수정 파일, 사용한 원천, 미확정 의존성, 후속 스킬 연계를 보고한다.

## `docs/trd.md` 역할

루트 TRD는 전체 FE 기술 허브다. 다음만 기록한다.

- 사용한 PRD/spec/architecture/contract/storyboard source와 확인 상태
- feature별 TRD 링크와 상태
- 공통 fixed architecture 제약 요약
- feature TRD가 공통으로 따라야 할 hard/conditional/advisory gate
- 공통 UI foundation 구현 요구와 후속 foundation 이슈 진입 가능 여부
- FE/BE 협의가 필요한 공통 기술 의존성
- 후속 `create-issues-adr` 진입 가능 여부

루트 TRD에 feature별 상세 상태 머신, API 필드 전체, 개별 테스트 케이스, issue slicing을 길게 쓰지 않는다.

## 기능별 TRD 작성 규칙

자세한 형식은 `references/trd-template.md`를 읽고 따른다.

- 기능 TRD는 `docs/features/{feature}/trd.md`에 작성한다.
- PRD의 사용자 목표를 반복 설명하는 데 그치지 말고, FE 구현자가 지켜야 할 기술 요구사항으로 변환한다.
- fixed architecture의 공통 정책을 다시 결정하지 않는다. 해당 feature에 적용되는 제약과 구체화만 기록한다.
- storyboard는 화면 의미, entry point, PC/Mobile 차이, interaction state를 추적하는 데 사용한다.
- 디자인 기준이 있으면 token/component pattern, responsive/a11y/visual acceptance를 추적한다. 기준이 없으면 구체적인 색상·spacing·typography 값을 만들지 않는다.
- REST/STOMP 계약은 fixed contract projection 또는 BE 요구사항 원천에 근거한 경우에만 쓴다.
- API endpoint, payload, message type, 에러 코드가 미확정이면 임의 이름을 만들지 말고 미확정 의존성으로 둔다.
- 테스트 섹션은 후속 issue/TDD가 어떤 관점을 가져야 하는지 적는다. 실제 테스트 파일명, TDD RED 결과, Given-When-Then AC는 `create-issues-adr`와 TDD 스킬 책임이다.
- 공통 token, primitive, app shell 같은 cross-feature 기반은 root TRD의 foundation handoff에 기록하고 개별 feature 구현에 중복시키지 않는다.
- 보안, 개인정보, 인증/권한, 실시간 연결, 캐시/동기화, 접근성 영향이 있으면 반드시 기술 요구사항 또는 미확정 항목으로 남긴다.

## 승인 게이트

- `docs/trd.md`를 생성하거나 갱신하기 전 hub 변경 요약을 제시하고 승인받는다.
- 각 `docs/features/{feature}/trd.md`를 생성하거나 갱신하기 전 feature별 기술 요구사항 요약, 미확정 의존성, 상위 산출물 재검토 필요 항목을 제시하고 승인받는다.
- 사용자가 "추천대로", "계속", "알아서"처럼 위임하면 추천 초안을 채택할 수 있다.
- 승인 전에는 다음 feature로 넘어가지 않는다.
- 승인 후에도 새 충돌이나 미확정 계약이 발견되면 즉시 멈추고 재확정한다.
- build/harness 설정 수정은 별도 요약과 승인을 받아야 한다. 사용자가 "추천대로", "계속", "알아서"처럼 위임하면 fixed architecture에 맞는 최소 설정 보정을 채택할 수 있다.

## 후속 스킬로 넘길 항목

- `create-issues-adr`: 확정된 feature TRD를 수직 슬라이스 이슈와 ADR 후보로 분해한다.
- `sync-fe-contracts`: BE fixed 협의 결과가 있지만 FE `docs/contracts/*` projection이 없을 때 실행한다.
- `architecture-decision`: TRD 작성 중 fixed architecture가 누락됐거나 새 공통 FE 정책 결정이 필요할 때 실행한다.
- `spec-read` 또는 BE 협의 재개: PRD와 요구사항 원천이 충돌하거나 REST/STOMP 계약이 확정되지 않았을 때 필요하다.

## 완료 보고

작업을 마치면 다음만 간결히 보고한다.

- 생성 또는 수정한 `docs/trd.md`
- 생성 또는 수정한 `docs/features/{feature}/trd.md`
- 사용한 PRD source와 `$spec-read` 사용 여부
- 사용한 fixed architecture 디렉터리
- 사용한 contract/storyboard source
- 수정한 build/harness 설정 파일과 검증 명령 결과
- 후속 `create-issues-adr` 진입 가능 feature
- 남은 미확정 의존성, 상위 산출물 재검토, FE/BE 협의 필요 항목
