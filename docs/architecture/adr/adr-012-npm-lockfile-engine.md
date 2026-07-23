---
id: "ARCH-ADR-012"
status: "accepted"
decision_scope: "harness"
fixed_reference: "docs/architecture/fixed-20260723/harness-fixed.md"
supersedes: []
source_documents:
  - "docs/architecture/interview-20260713/summary.md"
---

# ARCH-ADR-012. npm Lockfile과 Engine 고정

## Context

현재 단일 FE package이고 package manager/lockfile/Node version이 고정되지 않았다. local hook과 CI 재현성이 필요하다.

## Decision

npm을 사용하고 committed `package-lock.json`, `npm ci`, pinned Node LTS major와 npm version을 강제한다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| npm + npm ci | bootstrap 단순, 재현 가능 | workspace 격리·효율은 pnpm보다 약함 | 단일 app에 충분 | 선택 |
| pnpm | strict dependency, 효율 | 별도 bootstrap/version 관리 | workspace 이점 미확인 | 제외 |
| Yarn Berry | PnP, 강한 재현 | tool 호환·학습 비용 | 현재 필요 근거 없음 | 제외 |
| version 미고정 | 설정 적음 | local/CI drift | harness 신뢰성 저하 | 제외 |

## Consequences

lockfile 변경도 전체 check를 통과해야 한다. monorepo 전환이나 설치 성능 문제가 측정되면 pnpm을 재검토한다.
