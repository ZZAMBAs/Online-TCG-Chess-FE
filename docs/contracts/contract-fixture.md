# Contract Fixture FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/contract-fixture/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- canonical fixture schema가 outbound option, inbound transition, snapshot, outcome, definition view와 manifest/fingerprint의 source다.
- 카드/이벤트 payload는 자유형이 아니라 discriminated union이며 viewer-private sequence와 privacy 규칙을 따른다.
- board authority는 `resultingFen`이다. outcome 좌표를 다시 적용하지 않으며 perspective는 rendering/input 경계에서만 적용한다.
- source fingerprint와 manifest가 일치하지 않거나 schema/privacy 검증에 실패하면 fixture를 소비하지 않는다.

## FE Consumption Notes

- generated TypeScript/Ajv validator를 사용하고 수기 union 확장은 하지 않는다.
- 검증된 transition/snapshot만 reducer에 전달한다.
- FE 해석: fixture fingerprint 검증은 계약 drift 차단 경계로 취급한다.

## Excluded From FE Projection

- fixture 생성 스크립트, 서버 fixture 저장·배포와 CI 구현 절차.
