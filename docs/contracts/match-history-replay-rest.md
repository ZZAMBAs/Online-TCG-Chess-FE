# Match History Replay REST FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/match-history-replay-rest/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- match summary는 최대 10개 recent match page를 사용한다.
- sealed replay는 terminal, initialState, steps, stateAfter, visibleCardDefinitions의 closed DTO를 사용한다.
- `initialState`와 `stateAfter`는 동일 viewer-redacted state schema이며 live-only action capability, receipt, connection metadata를 포함하지 않는다.
- replay state는 current card handler를 실행하거나 outcome 좌표를 재적용하지 않고 서버 state를 소비한다.

## FE Consumption Notes

- replay board는 `stateAfter`를 원자 교체한다.
- board rotation은 viewer color를 bottom에 두는 rendering 경계에서만 수행하고 canonical FEN/좌표는 변경하지 않는다.

## Excluded From FE Projection

- replay sealing, persistence와 server history query 구현.
