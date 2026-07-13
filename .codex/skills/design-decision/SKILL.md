---
name: design-decision
description: Online-TCG-Chess-FE에서 구조 승인된 storyboard를 실제에 가까운 통합 화면으로 렌더링하기 위한 Git 기반 디자인 baseline을 draft로 만들고, 시각 검토 후 approved로 확정한다. $create-storyboard 내부 디자인 패스 또는 독립 재검토에서 semantic token, typography, spacing, responsive, a11y, 공통 UI variant와 foundation handoff를 결정할 때 사용한다.
---

# Design Decision

## 역할

- `$create-storyboard`의 내부 디자인 패스로 동작하며 독립 재검토도 지원한다.
- 구조 승인된 화면을 입력으로 `design-baseline.md`와 공유 CSS 계약을 만든다.
- draft baseline으로 storyboard를 시각화한 뒤 사용자 시각 승인과 함께 approved로 확정한다.
- 실제 `src`, package, architecture, TRD는 수정하지 않는다.

## 시작 절차

1. `$spec-read`와 `$prd-read` 최신성을 확인한다. 하나라도 실패하면 중단한다.
2. `references/baseline-template.md`를 읽는다.
3. manifest, pages, fragments, storyboard, 기존 baseline과 사용자가 명시적으로 제공한 외부 참고 자산을 읽는다.
4. 포함할 모든 페이지의 `review.structure`이 `approved`인지 확인한다. 하나라도 아니면 해당 page id를 보고하고 구조 검토로 돌아간다.
5. 기존 baseline은 source hash와 storyboard 구조 변경 여부를 비교해 갱신한다.

## 결정 범위

- 시각 방향과 정보 밀도
- semantic color, typography, spacing, radius, elevation scale
- Button, Input, Dialog/Sheet, Card, Status, Navigation variant와 상태
- 체스 보드, TCG 카드, 채팅, 관리자 표의 공통 시각 문법
- desktop/mobile breakpoint, touch target, focus, contrast, keyboard, reduced motion
- 디자인 source of truth와 foundation/feature handoff
- storyboard page와 대표 상태의 component pattern 매핑

## Draft와 승인

- 구조 승인 후 `status: draft` baseline을 작성할 수 있다.
- draft 값은 storyboard 시각 검토에만 사용하며 production 확정 근거가 아니다.
- `$create-storyboard`가 draft baseline으로 모든 페이지를 시각화한다.
- 모든 `review.visual`이 승인되고 사용자가 디자인 기준을 승인한 뒤에만 baseline을 `approved`로 바꾼다.
- 구조가 변경되면 관련 시각 승인과 baseline 영향 범위를 다시 검토한다.

## 산출물

- `docs/design/design-baseline.md`: draft/needs-review/approved 권위 문서
- `docs/design/storyboard/styles/tokens.css`: baseline의 semantic token 표현
- `docs/design/storyboard/styles/primitives.css`: 공통 UI primitive 검토 표현
- `docs/design/storyboard/styles/product-surfaces.css`: 제품 고유 표면 검토 표현
- `docs/design/design-specimen.html`: 공통 primitive만 별도로 비교할 필요가 있을 때 선택적으로 생성

공유 CSS는 storyboard 검토 구현이며 production CSS 기술이나 파일 위치를 확정하지 않는다. 승인된 값과 variant 계약만 후속 구현이 소비한다.

## 질문과 진행

- 요구사항과 구조에서 결정할 수 없는 전역 선택만 한 번에 하나씩 묻고 추천안을 먼저 제시한다.
- 시각 방향과 density를 먼저, token과 component variant를 다음으로 결정한다.
- 사용자가 추천안에 위임하면 채택해 draft를 진행할 수 있다.
- 디자인 값과 화면 결과를 보지 않은 상태에서 approved를 요청하지 않는다.

## 후속 handoff

- `$architecture-decision`: production CSS 기술, token 위치, component boundary, catalog/visual gate
- `$create-trd`: feature별 responsive/a11y/visual acceptance
- foundation issue/TDD: 실제 token, primitive, app shell 구현

## 금지 사항

- 기능 API, payload, domain 정책, 앱 framework를 결정하지 않는다.
- 페이지별 CSS나 모든 상태의 고충실도 복제본을 만들지 않는다.
- draft 값을 승인된 구현 기준으로 표시하지 않는다.
- 사용자 승인 없이 baseline 또는 visual review를 approved로 바꾸지 않는다.
