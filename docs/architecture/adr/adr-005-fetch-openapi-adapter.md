---
id: "ARCH-ADR-005"
status: "accepted"
decision_scope: "frontend-architecture"
fixed_reference: "docs/architecture/fixed-20260713/impl-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-005. Fetch Transport와 OpenAPI Adapter

## Context

same-site session cookie, CSRF, timeout/cancel과 공통 REST 오류를 일관되게 처리해야 한다. fixed OpenAPI 위치는 아직 없다.

## Decision

표준 `fetch` 공통 transport 뒤에 generated OpenAPI client와 feature adapter를 둔다. 전체 요청 timeout은 AbortSignal로 강제하고 변경 요청은 멱등성 근거 없이 retry하지 않는다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| fetch + generated + adapter | 표준 기반, 경계 명확 | transport를 얇게 작성 | JSON REST와 session auth에 적합 | 선택 |
| Axios interceptor | 익숙한 option/interceptor | dependency와 interceptor 집중 | 단계별 전송 요구가 없음 | 제외 |
| generated client 직접 사용 | 코드 적음 | generator 응답·오류가 feature에 노출 | 교체·test 경계 약화 | 제외 |
| feature별 fetch | 빠른 시작 | credential/CSRF/error 중복 | 정책 drift 위험 | 제외 |

## Consequences

transport fixture test가 필요하다. upload progress, idle/read timeout이나 대용량 streaming 요구가 생기면 Axios 또는 별도 transport를 재검토한다.
