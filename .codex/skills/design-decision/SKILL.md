---
name: design-decision
description: Online-TCG-Chess-FE에서 $create-storyboard 승인 후 $architecture-decision 전에 Figma 없이 Git 기반 FE 디자인 기준을 승인형으로 확정해야 할 때 사용한다. BE 요구사항과 PRD, storyboard를 읽어 docs/design/design-baseline.md를 생성·갱신하고, 시각 방향, semantic token 값, typography·spacing·responsive·a11y·공통 UI variant·foundation handoff를 한국어로 결정하며, 필요 시 선택적 design specimen을 만들고 사용자 승인 후에만 기준 상태를 approved로 표시한다.
---

# Design Decision

## 역할

- `$design-decision`은 AI가 디자인과 FE를 함께 수행할 때 Git 안에서 시각 디자인 기준을 확정하는 승인형 workflow다.
- `$create-storyboard`의 화면 의미·상태·PC/Mobile 구조를 입력으로 받고, `$architecture-decision`이 소비할 디자인 기준을 만든다.
- Figma나 외부 디자인 서비스는 필수가 아니다. 외부 참고 자산이 있으면 source와 사용 범위만 기록한다.
- 실제 `src` CSS, token, UI primitive, package/하네스는 수정하지 않는다. 구현은 후속 foundation/feature TDD GREEN이 담당한다.

## 시작 절차

1. `$spec-read`로 BE `master` 요구사항 최신성을 확인한다. 실패하면 요구사항 기반 결정을 중단한다.
2. `$prd-read`로 hub와 관련 feature PRD 최신성을 확인한다. 실패하면 중단한다.
3. `references/baseline-template.md`를 읽는다.
4. 존재하는 `docs/design/storyboard-manifest.json`, `storyboard-pages.md`, `storyboard.html`, `storyboard/fragments/*`, 기존 `design-baseline.md`, 외부 참고 자산 경로를 읽는다.
5. storyboard가 없으면 화면·상태 근거가 부족한 것으로 보고 `$create-storyboard`를 먼저 요청한다. 기존 상세 시안이나 Figma가 없다는 이유만으로는 중단하지 않는다.
6. manifest가 있으면 이번 baseline에 포함할 모든 page의 `status`가 `approved`인지 확인한다. `draft`, `needs-review`, `needs-revision` 또는 누락 상태가 하나라도 있으면 해당 page id와 사유를 제시하고 `$create-storyboard` 검토·승인으로 되돌아간다. 승인 범위를 임의로 축소하지 않는다.
7. 기존 baseline이 있으면 source hash, 승인 상태, storyboard와의 차이를 확인하고 중복 생성 대신 갱신한다.

## 결정 범위

- 제품 시각 방향과 정보 밀도
- semantic color, typography, spacing, radius, elevation의 token 값 또는 scale
- Button, Input, Dialog/Sheet, Card, Status message, Navigation의 variant와 상태 규칙
- 체스 보드·TCG 카드·관리자 표처럼 제품 고유 표면의 우선순위와 금지 사항
- desktop/mobile breakpoint, touch target, focus, contrast, keyboard, reduced motion 기준
- 디자인 source of truth, token 소유 위치, style 우회 금지, foundation/feature handoff
- storyboard page id와 대표 상태가 어떤 component pattern을 소비하는지

## 결정하지 않는 범위

- 기능별 API/STOMP payload, domain 정책, 화면 문구
- `src`의 실제 CSS 또는 component 구현
- framework, CSS 기술, router, state management, build/CI 결정
- 모든 화면의 고충실도 mockup 또는 페이지별 CSS 복제
- 외부 Figma 프로젝트 생성·동기화

## 사용자 질문과 승인

- 요구사항이나 storyboard로 결정할 수 없는 디자인 선택지만 한 번에 하나씩 질문한다.
- 질문마다 추천안을 먼저 제시하고, 색상·density·시각 방향처럼 기준 전체에 영향을 주는 결정부터 묻는다.
- 결정 초안에는 확정값, 미확정값, 영향을 받는 storyboard page id, foundation 구현 handoff를 요약한다.
- 사용자 승인 전에는 `design-baseline.md`의 `status`를 `approved`로 표시하지 않는다.
- 사용자가 "추천대로", "계속", "알아서"처럼 위임하면 추천안을 채택할 수 있다.

## 산출물

- `docs/design/design-baseline.md`: 권위 있는 Git 기반 디자인 기준
- `docs/design/design-specimen.html`: 사용자 요청 또는 승인된 시각 검토 필요 시에만 만드는 선택적 공통 UI specimen

`design-specimen.html`은 Button/Input/Dialog/Card/Status와 제품 고유 표면 일부를 공유 CSS로 보여주는 보조 자료다. 화면별 mockup이나 production CSS의 복제본으로 만들지 않는다.

## 진행 절차

1. 입력 최신성과 storyboard 승인 상태를 확인한다. 승인되지 않은 포함 대상 page가 있으면 baseline 초안·파일 작성·후속 handoff를 하지 않는다.
2. page별 `fidelity`, `representative_states`, `component_patterns`를 읽어 디자인 영향이 큰 화면을 고른다.
3. baseline 초안을 만들고 시각 방향, token scale, component variant, responsive/a11y, handoff, 미확정 항목을 정리한다.
4. 파일 작성 전 초안 요약과 선택적 specimen 필요 여부를 사용자에게 제시하고 승인받는다.
5. 승인된 `docs/design/design-baseline.md`만 생성 또는 갱신한다.
6. specimen이 승인된 경우에만 최소 공유 CSS로 생성하고, 기준 문서보다 권위가 낮음을 기록한다.
7. baseline의 source, 상태, page/component traceability, foundation handoff가 빠지지 않았는지 확인한다.

## 후속 handoff

- `$architecture-decision`: CSS 기술, token 저장 위치, component boundary, catalog/visual gate를 fixed architecture로 확정한다.
- `$create-trd`: baseline을 feature별 token/component/responsive/a11y/visual acceptance 요구사항으로 추적한다.
- `$create-issues-adr foundation`: token, primitive, app shell의 검증 가능한 foundation 이슈를 만든다.
- `$tdd-green`: approved baseline과 fixed architecture를 따라 실제 `src` token/CSS/primitive를 구현한다.

## 금지 사항

- storyboard, BE 요구사항, PRD 원문, architecture, TRD, 앱 소스코드를 수정하지 않는다.
- 승인되지 않은 디자인 값을 foundation 또는 feature 구현의 확정 근거로 표시하지 않는다.
- 모든 화면을 고충실도 HTML/CSS로 만들거나 페이지별 CSS를 중복 작성하지 않는다.
- 디자인 기준 없이 구현 기술 또는 실제 CSS 값을 임의 확정하지 않는다.
