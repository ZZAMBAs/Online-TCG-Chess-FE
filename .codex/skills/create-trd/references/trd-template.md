# TRD Template

기능별 TRD를 작성하거나 갱신할 때 이 구조를 따른다. 섹션명은 유지하되, 근거가 없는 항목은 추정하지 말고 `미확정`으로 남긴다.

```markdown
# {Feature Name} TRD

## Source Traceability

- prd_source:
- spec_source:
- architecture_source:
- contract_sources:
- storyboard_sources:
- last_verified:

## Status

- trd_status: draft | approved | blocked
- approval:
- blockers:

## Technical Goal

## Non-Goals

## Architecture Constraints

## Route and Screen Responsibility

## Component and Module Responsibility

## State Ownership and Lifecycle

## REST/API Client Requirements

## STOMP/Realtime Requirements

## Error, Loading, Empty, and Permission Behavior

## UI Interaction and Storyboard Traceability

## Security, Privacy, and Abuse Considerations

## Accessibility and Responsive Requirements

## Test Strategy for Issue Slicing

## Unresolved Dependencies
```

## 작성 기준

- `Source Traceability`에는 실제로 확인한 문서 경로와 commit/hash/manifest 정보를 가능한 범위에서 남긴다.
- `Status`의 `approved`는 사용자 승인 후에만 사용한다.
- `Technical Goal`은 구현자가 무엇을 기술적으로 만족해야 하는지 적는다.
- `Non-Goals`에는 이 feature TRD가 결정하지 않는 영역을 적는다.
- `Architecture Constraints`에는 fixed architecture에서 상속한 Hard/Conditional/Advisory gate를 feature 관점으로 요약한다.
- REST/STOMP 섹션은 해당 feature에 없으면 `해당 없음`으로 둔다.
- 미확정 endpoint, payload, message type, error code, 권한 정책은 이름을 만들지 말고 `Unresolved Dependencies`에 owner와 필요한 후속 절차를 적는다.
- `Test Strategy for Issue Slicing`은 후속 `create-issues-adr`가 이슈별 Given-When-Then과 TDD 테스트 관점으로 쪼갤 수 있는 수준으로 쓴다.
