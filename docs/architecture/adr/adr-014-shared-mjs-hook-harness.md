---
id: "ARCH-ADR-014"
status: "accepted"
decision_scope: "harness"
fixed_reference: "docs/architecture/fixed-20260713/harness-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-014. Hook과 CI 공유 MJS Harness

## Context

local feedback은 빨라야 하지만 CI가 최종 권위여야 한다. hook 전용 shell logic은 CI와 drift하기 쉽다.

## Decision

pre-commit staged fast check, pre-push changed-scope check, CI full check가 같은 Node `.mjs` entrypoint를 mode만 달리해 사용한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| shared MJS entry | CI 재사용·fixture test | file collection 규칙 필요 | cross-platform harness에 적합 | 선택 |
| hook 전체 검사 | 높은 local 신뢰 | 느려 우회 증가 | E2E/build 규모에 부적합 | 제외 |
| CI only | 설정 단순 | feedback 늦음 | 개발 loop 저하 | 제외 |
| shell inline | 빠른 시작 | 인자·platform·test 취약 | CI drift 위험 | 제외 |

## Consequences

entrypoint는 `--files/--all`, 중앙 ignore, rule id와 exit 0/1/2를 제공하고 fixture test를 갖는다. Node 실행 자체가 병목이 되면 구현을 재검토한다.
