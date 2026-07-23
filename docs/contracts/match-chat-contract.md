# Match Chat FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/match-chat-contract/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- current-game chat history REST와 live STOMP delivery는 `ChatMessageView` 및 closed command/error schema를 사용한다.
- history/live merge는 message sequence와 idempotency를 기준으로 중복 없이 수행한다. sequence gap은 game-state resync가 아니라 chat 복구 오류로 처리하지 않는다.
- `matchChatVisible` off는 unsubscribe/UI hide, on은 subscribe → history → live merge 순서를 따른다.
- block, restriction, visibility와 rate limit 오류는 공통 error code로 소비한다.

## FE Consumption Notes

- chat cache/buffer/reducer/pending을 gameplay state에서 분리한다.
- generated REST/STOMP schema와 Ajv validation을 사용한다.

## Excluded From FE Projection

- chat retention, publish transaction, moderation/block 판정 구현.
