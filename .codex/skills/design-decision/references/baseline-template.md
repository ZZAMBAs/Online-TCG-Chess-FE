# Design Baseline Template

```markdown
# Online TCG Chess Design Baseline

## Source Traceability

- spec_source:
- prd_sources:
- storyboard_manifest:
- storyboard_structure_approval:
- visual_references:
- last_verified:

## Status

- status: draft | needs-review | approved | blocked
- visual_review:
- approval:
- blockers:

## Design Source of Truth

- authoritative_artifact: docs/design/design-baseline.md
- storyboard_preview: docs/design/storyboard.html
- review_css:
  - docs/design/storyboard/styles/tokens.css
  - docs/design/storyboard/styles/primitives.css
  - docs/design/storyboard/styles/product-surfaces.css
- production_owner: foundation and feature TDD GREEN

## Visual Direction and Density

## Semantic Tokens

### Color

### Typography

### Spacing, Radius, Elevation

## Component and State Grammar

- App shell and navigation:
- Button:
- Input and validation:
- Dialog and sheet:
- Card, list and table:
- Status, loading, empty and permission:
- Chess board and game HUD:
- TCG card and hand:
- Chat and admin workspace:

## Responsive and Accessibility Baseline

- breakpoint and density:
- touch target:
- focus and keyboard:
- contrast and semantic color:
- motion:

## Storyboard Traceability

| page id | representative states | component patterns | visual review |
| --- | --- | --- | --- |

## Foundation Handoff

- semantic token contract:
- shared UI primitives:
- product surfaces:
- app shell:
- token bypass policy:

## Feature Handoff

- feature composition rules:
- visual acceptance candidates:

## Unresolved Decisions
```

## 작성 규칙

- source와 구조 승인 근거를 먼저 기록한다.
- draft baseline은 storyboard 시각 검토용이며 production 확정값이 아님을 명시한다.
- token은 이름, 의미, 값/scale과 사용 금지를 함께 기록한다.
- 외부 참고 자산은 사용자가 명시적으로 제공한 경우에만 경로와 채택 범위를 기록하며 독립 CSS를 권위로 삼지 않는다.
- storyboard에 없는 페이지를 추가하지 않는다.
- 모든 visual review와 사용자 승인이 끝난 뒤에만 approved로 바꾼다.
- 승인된 계약과 검토용 CSS, 실제 production 소유 위치를 구분한다.
