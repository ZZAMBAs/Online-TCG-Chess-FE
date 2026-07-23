# Matchmaking Lifecycle FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/matchmaking-lifecycle/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- matchmaking REST join/cancel과 개인 STOMP event는 idempotency와 monotonic version을 사용한다.
- duplicate event는 무시하고 version gap/unknown entry는 GET baseline으로 확인한다.
- `GAME_CREATED`를 확인하면 같은 `gameId`로 한 번만 route handoff하고 matchmaking 구독을 종료한 뒤 game-state sync로 전환한다.
- active game이 있으면 `409 GAME_IN_PROGRESS`이며 own active `gameId`로 route 복구할 수 있다.
- queue entry는 single saved deck의 ID/revision/current validity를 검증하고 대기 중 변경은 `DECK_CHANGED`/`DECK_INVALID` terminal 상태다.

## FE Consumption Notes

- REST baseline은 query가, live 상태는 feature reducer가 소유한다.
- pending 중 중복 입력을 막되 server idempotency를 최종 안전장치로 사용한다.

## Excluded From FE Projection

- queue serialization, game handoff transaction과 candidate filtering 구현.
