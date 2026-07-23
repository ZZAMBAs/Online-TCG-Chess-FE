# Game Command Catalog FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/game-command-catalog/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- command, transition, event, receipt와 pending은 canonical catalog의 closed union이다.
- public transition은 원자 commit이고 private event는 actor-private instance/sequence를 보강한다. duplicate와 idempotent augmentation을 구분한다.
- 공개 손패는 public transition으로 갱신하고 private event로 상대 정보나 공개 손패를 추정하지 않는다.
- FEN은 렌더링 입력이며 FE가 legality 재검증·정상화로 계약값을 변경하지 않는다.
- countdown은 server time/deadline anchor 기반이며 client tick은 server state가 아니다.

## FE Consumption Notes

- feature reducer가 public transition, private augmentation, pending overlay와 receipt를 분리한다.
- FE 해석: schema/generated catalog 외 자유형 mock은 계약 소비로 보지 않는다.

## Excluded From FE Projection

- command 처리 순서의 서버 구현, game domain과 transaction 세부.
