# Design Baseline Template

```markdown
# Online TCG Chess Design Baseline

## Source Traceability

- spec_source:
- prd_sources:
- storyboard_sources:
- external_references:
- last_verified:

## Status

- status: draft | needs-review | approved | blocked
- approval:
- blockers:

## Design Source of Truth

- authoritative_artifact: docs/design/design-baseline.md
- reference_artifacts:
- production_owner: foundation and feature TDD GREEN

## Visual Direction and Density

## Semantic Tokens

### Color

### Typography

### Spacing, Radius, Elevation

## Component and State Grammar

- Button:
- Input and validation:
- Dialog and sheet:
- Card, list, table:
- Status, loading, empty, permission:
- Chess board and TCG card surfaces:

## Responsive and Accessibility Baseline

- breakpoint and density:
- touch target:
- focus and keyboard:
- contrast and semantic color:
- motion:

## Storyboard Traceability

| page id | representative states | component patterns | design impact |
| --- | --- | --- | --- |

## Foundation Handoff

- token and style entry:
- shared UI primitives:
- app shell:
- token bypass policy:

## Feature Handoff

- feature-specific composition rules:
- visual acceptance candidates:

## Unresolved Decisions
```

## 작성 규칙

- source와 approval 상태를 먼저 기록한다.
- token은 이름, 의미, 값 또는 scale, 사용 금지를 함께 기록한다.
- 제품 고유 표면은 실제 카드 아트나 게임 규칙을 만들지 않고 정보 위계·상태 표현·접근성 기준만 기록한다.
- storyboard에 없는 화면 레이아웃을 추가하지 않는다.
- 미확정 값은 추정으로 채우지 않고 owner와 후속 단계로 남긴다.
