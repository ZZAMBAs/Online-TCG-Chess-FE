---
name: architecture-review
description: Online-TCG-Chess-FE의 FE 구현 아키텍처, FE 서버/배포 인프라, CI/CD, 정적 분석, Git hook mjs 하네스, 테스트/계약 드리프트 게이트 문서를 한국어로 검토하고 승인 후 보완해야 할 때 사용한다. 기존 architecture-review-ledger와 현재 산출물·FE 코드·설정 fingerprint를 비교해 변경 없는 영역은 생략하고, 라우팅/상태/API/STOMP/스타일링/배포/하네스 중 바뀐 영역은 재검토해야 할 때 사용한다.
---

# Architecture Review

## 개요

FE 구현 아키텍처, FE 서버/배포 인프라, CI/CD, 정적 분석과 AI 하네스 산출물을 변경 영향 기반으로 검토하고, 승인된 보완 사항은 아키텍처 문서에 반영한다. 매번 전체를 재검토하지 않고, 이전 리뷰 이후 바뀐 영역만 깊게 본다.

## 기본 원칙

- 모든 검토와 요약은 한국어로 작성한다.
- 기존 `docs/architecture/architecture-review-ledger.md`가 있으면 먼저 읽는다.
- 리뷰 단위는 문서 전체가 아니라 FE 아키텍처 영역이다.
- 변경 없는 영역은 생략할 수 있다.
- 관련 요구사항, PRD/TRD, storyboard, 인터페이스 계약, 아키텍처 결정, FE 코드, 의존성, CI/CD, 배포/인프라 설정 중 하나라도 바뀌면 생략하지 않는다.
- 생략한 영역도 생략 사유와 재검토 조건을 남긴다.
- BE 요구사항 판단이 필요하면 `$spec-read`로 최신성을 확인한다. 실패하면 요구사항 기반 검토를 중단한다.
- 파일 작성 전에는 반영 예정 요약을 세션에 제시하고 승인받는다.
- 개별 스킬 내부에 전체 워크플로우 순서를 강제하지 않는다.
- `$architecture-decision` 안에서 실행될 때는 아키텍처 ADR의 대안 비교, 상태, fixed 연결과 drift를 검토한다. ADR 파일 생성과 상태 전이는 오케스트레이터가 소유한다.
- issue 분리, feature 구현 ADR, 심층 보안 리뷰, 운영 runbook 작성은 직접 수행하지 않고 후속 스킬 연계 항목으로 표시한다.

## 먼저 확인할 자료

존재하는 파일만 읽는다.

- `AGENTS.md`
- `docs/design/storyboard-manifest.json`, `docs/design/storyboard-pages.md`, `docs/design/storyboard/fragments/*`
- `.cache/prd-read/docs/prd.md`, `docs/trd.md`, `docs/websocket-spec.md`
- `.cache/prd-read/docs/features/*/prd.md`, `docs/features/*/trd.md`
- `docs/architecture/*`
- `docs/architecture/adr/*.md`, `docs/architecture/adr-index.md`
- `package.json`, lockfile, `src`, `app`, `components`, `pages`, `routes`
- `vite.config.*`, `next.config.*`, `nuxt.config.*`, `tsconfig*.json`
- `eslint.config.*`, `.eslintrc*`, `prettier.config.*`, `.prettierrc*`
- `tailwind.config.*`, `postcss.config.*`, style/theme/token files
- `docs/design/design-baseline.md`, 존재하는 경우의 `docs/design/design-specimen.*`
- `vitest.config.*`, `playwright.config.*`, `cypress.config.*`
- `.husky`, `.lintstagedrc*`, hook/helper `.mjs` files
- `.github`, `Dockerfile`, `docker-compose*`, `infra`, `deploy`, hosting config

## Fingerprint

필요하면 `scripts/architecture_fingerprint.py`를 사용해 관련 파일과 디렉터리의 fingerprint를 계산한다.

`design-baseline.md`가 없거나 `approved`가 아니면 디자인 시스템·스타일링 구현 경계 검토를 `review-blocked`로 기록한다.

```bash
python3 .codex/skills/architecture-review/scripts/architecture_fingerprint.py package.json src .github docs/architecture
```

이 스크립트는 읽기 전용이어야 하며 repo 파일을 수정하지 않는다.
- ledger에는 영역별 `watched_paths`, `ignored_paths`, `contract_sources`, `ci_checks`를 남겨 다음 리뷰의 생략 판단 근거로 사용한다.

## 리뷰 영역

다음 영역별로 검토한다.

- FE app runtime과 build tool
- TypeScript configuration
- routing과 route boundary
- state management와 server cache
- API client와 error/auth handling
- STOMP/WebSocket client
- module/import boundaries
- component architecture
- styling/design system boundary
- FE server, hosting, CDN, reverse proxy
- environment strategy와 runtime config
- security headers와 public secret 방지
- client observability와 sourcemap 정책
- CI/CD
- Git hook mjs harness
- static analysis와 lint
- test strategy와 quality gates
- contract drift gates
- generated client와 mock drift gates
- BE contract collaboration protocol
- dependency와 supply-chain policy
- release gates와 preview/stage/prod 전략

## 생략 가능 조건

다음이 모두 참이면 해당 영역은 생략할 수 있다.

- 관련 원천 문서가 변하지 않았다.
- 관련 PRD/TRD/storyboard 또는 인터페이스 계약이 변하지 않았다.
- 관련 아키텍처 결정이 변하지 않았다.
- 관련 FE 코드 또는 설정이 변하지 않았다.
- 관련 의존성, CI/CD, 배포/인프라 설정이 변하지 않았다.
- 이전 결정과 현재 문서가 충돌하지 않는다.

## 생략 금지 조건

다음 중 하나라도 참이면 재검토한다.

- 요구사항, PRD/TRD, storyboard가 바뀌었다.
- FE 코드나 설정이 문서와 다르다.
- 라우팅, 상태 관리, API client, STOMP client, 모듈 경계, 스타일링 방식이 바뀌었다.
- 디자인 기준 source, token 소유 경계, foundation 구현 handoff가 바뀌었다.
- 배포 형태, hosting/CDN/reverse proxy, env strategy, security header 정책이 바뀌었다.
- typecheck/lint/test/e2e/contract drift required check가 바뀌었다.
- OpenAPI/STOMP schema source, generated client, MSW mock, breaking change 절차가 바뀌었다.
- dependency, package manager, lockfile, engine policy가 바뀌었다.
- Git hook mjs guard나 lint-staged 정책이 바뀌었다.
- 이전에 `미확정`이던 항목이 확정되었다.
- fixed 문서의 결정과 ADR의 선택·상태·대체 관계가 다르거나, 의미 있는 대안 비교가 ADR에 누락되었다.

## 종합 응답 형식

```markdown
검토 범위:
- [검토한 영역]
- [생략한 영역과 사유]

핵심 이슈:
- [문제 또는 충돌]

추천 확정안:
- [반영할 정책 또는 문장]

ADR 검토:
- [결정별 ADR 필요 여부, 대안 비교 완전성, fixed 연결, 상태·대체 관계]

재검토 필요:
- [상위 산출물 또는 아키텍처 영역]

Ledger 반영 후보:
- [area, watched_paths, ignored_paths, contract_sources, ci_checks, fingerprint, skip_conditions, re_review_triggers 요약]
```

`references/review-ledger-schema.md`를 읽고 ledger 필드를 맞춘다.

## 문서 보완 규칙

- 사용자 승인 전에는 파일을 수정하지 않는다.
- 승인된 리뷰 결과만 `docs/architecture/*`에 반영한다.
- 기존 문서를 덮어쓰기보다 검토 결과에 맞춰 갱신한다.
- 원천 문서에 없는 값을 임의 확정하지 않는다.
- 요구사항, PRD/TRD, storyboard, 인터페이스 계약 변경이 필요하면 직접 수정하지 않고 재검토 필요 항목으로 남긴다.
- 아키텍처 ADR 보완이 필요하면 ADR id, 누락된 대안·근거, 필요한 상태 전이와 fixed 연결을 리뷰 결과에 명시한다. feature 구현 ADR, 심층 보안 리뷰, 운영 runbook은 후속 스킬 연계 항목으로 남긴다.
- accepted ADR과 fixed 문서의 선택이 다르면 `review-pass`로 판정하지 않는다.
- `architecture-review-ledger.md`에는 검토한 영역, 생략한 영역, 생략 사유, fingerprint, 재검토 조건을 남긴다.
