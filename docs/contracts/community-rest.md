# Community REST FE Contract

## Source

- source_repo: https://github.com/ZZAMBAs/Online-TCG-Chess-BE
- source_path: docs/negotiation/community-rest/summarize.md
- source_status: fixed
- source_session_status: completed
- source_commit: 0eff57d6590d5c8817355a0c71c465d1478be7bc
- source_verification: verified by canonical remote HEAD

## Status

fixed projection.

## FE-Relevant Contract

- 목록·검색·상세·생성·수정·삭제는 닫힌 `CommunityPostView`와 공통 오류 계약을 사용한다.
- 목록은 cursor 기반 ordering을 사용하고 detail은 masking/concealment 상태를 포함한 authoritative view를 반환한다.
- 본문 길이와 plain-text 규칙을 따른다. list에서만 line clamp를 적용하고 detail/cache 값은 변형하지 않는다.
- PATCH는 dirty field를 하나 이상 포함해야 하며 stale revision conflict 시 server 최신 상태와 local draft를 구분한다.
- 권한·삭제·moderation 상태는 서버가 최종 결정하며 숨겨진 리소스는 동일 not-found 의미로 처리된다.

## FE Consumption Notes

- generated REST client와 TanStack Query가 full masked view를 소유한다.
- conflict에서는 local draft를 유지한 채 refetch하며 자동 merge/retry하지 않는다.

## Excluded From FE Projection

- moderation persistence, masking 알고리즘과 transaction/query 구현.
