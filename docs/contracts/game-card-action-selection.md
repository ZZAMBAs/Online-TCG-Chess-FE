# Game Card Action Selection FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/game-card-action-selection/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- 카드 action은 fixed command/selection schema와 상태 전이를 사용하며 과거의 자유형 `{cardInstanceId,selection}` 또는 `CARD_USED` 가정으로 확장하지 않는다.
- public transition, actor-private augmentation, local selection draft와 pending overlay는 서로 다른 데이터다.
- 카드별 selection interaction과 public/private outcome은 generated exhaustive union으로 처리한다.
- board perspective와 card definition/version은 canonical catalog/deck/replay contract를 따른다.

## FE Consumption Notes

- 권위 transition과 private augmentation을 분리해 merge한다.
- FE 해석: contract-fixture와 active card/deck/replay 계약이 함께 제공될 때만 완전한 action UI를 소비할 수 있다.

## Excluded From FE Projection

- 카드 effect handler, 서버 상태 전이와 persistence, 구현 gate 절차.
