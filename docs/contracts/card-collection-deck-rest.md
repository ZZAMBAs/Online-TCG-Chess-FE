# Card Collection Deck REST FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/card-collection-deck-rest/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- `GET /api/v1/cards/catalog`은 active `CardDefinitionView`와 `catalogViewFingerprint`를 반환한다. collection/deck/reward는 stable `cardId`로 catalog와 join한다.
- `GET /api/v1/me/card-collection`은 `{revision,entries[{cardId,quantity}]}` 완전 resource다.
- `GET /api/v1/card-packs/basic`은 `BASIC`, 3장 opening, probability version과 KST quota를 반환한다.
- `POST /api/v1/card-packs/basic/openings`은 정확히 `{}`와 CSRF, `Idempotency-Key`를 사용한다. 최초 성공과 같은 key replay는 최초 terminal result를 반환한다.
- opening reward는 slot 1·2·3의 literal quantity `1`이며 current catalog와 join한다. success/replay 후 collection과 pack 상태를 재조회한다.
- 사용자는 하나의 saved deck을 가지며 deck revision conflict와 current validity를 UI에서 구분해야 한다.

## FE Consumption Notes

- catalog, collection, pack, deck은 독립 loading/error 상태를 갖는다.
- opening 중 중복 입력을 막고 불명확한 결과는 같은 key로 재시도한다.
- FE 해석: catalog 누락은 empty가 아니라 contract/catalog integrity 오류다.

## Excluded From FE Projection

- RNG, quota 지급 transaction, idempotency receipt 저장과 persistence 세부.
