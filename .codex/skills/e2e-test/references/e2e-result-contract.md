# E2E Result Contract

`e2e-test.md`는 최신 결과만 유지한다.

```markdown
# E2E Test: {issue-id}

## Status

- result: e2e-pass | e2e-failed | e2e-blocked | e2e-not-required
- e2e_required:
- issue_slice_type:

## Sources

- design_baseline:
- architecture:
- storyboard:
- trd:
- green_result:
- blue_result:

## Executed Coverage

| viewport | user flow | representative state | result | evidence summary |
| --- | --- | --- | --- | --- |

## Commands

- command:
- result:

## Visual and Accessibility Findings

- baseline comparison:
- keyboard/focus:
- mobile/desktop difference:

## Artifacts

- temporary screenshots/traces/videos deleted: true | false
- retained artifacts and approval:

## Blockers or Follow-up
```

## 작성 규칙

- `e2e_required: false`면 실행하지 않고 `e2e-not-required`와 판단 근거만 기록한다.
- screenshot 파일 경로를 장기 근거로 기록하지 않는다. 보관 승인된 artifact만 경로와 사유를 기록한다.
- visual failure는 viewport, 사용자 행동, 기대한 baseline/storyboard 상태, 실제 결과를 함께 적는다.
- 환경·브라우저·fixture 문제는 구현 결함과 구분한다.
