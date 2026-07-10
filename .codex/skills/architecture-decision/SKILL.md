---
name: architecture-decision
description: Online-TCG-Chess-FE에서 $architecture-interview와 $architecture-review를 하나의 승인형 워크플로로 묶어 FE 구현 아키텍처, FE 서버/배포 인프라, CI/CD, 정적 분석, Git hook mjs 하네스, 테스트/계약 드리프트 게이트를 확정해야 할 때 사용한다. 인터뷰 산출물을 리뷰하고, 리뷰 보완 사항이 있으면 최대 3회까지 인터뷰 방식으로 재수정 후 재리뷰하며, docs/architecture/interview-{yyyymmdd}/와 docs/architecture/fixed-{yyyymmdd}/ 및 current-fixed.md에 추적 가능한 결정 문서를 남겨야 할 때 사용한다.
---

# Architecture Decision

## 개요

`architecture-interview`와 `architecture-review`를 순서대로 실행해 FE 아키텍처 결정을 확정한다. 이 스킬은 하위 스킬을 대신하지 않고, 실행 순서, 반복 제한, 날짜별 추적 문서, 최종 fixed 문서의 위치와 완료 조건을 관리한다.

## 기본 원칙

- 모든 질문, 요약, 문서는 한국어로 작성한다.
- 먼저 `.codex/skills/architecture-interview/SKILL.md`와 `.codex/skills/architecture-review/SKILL.md`를 읽고 따른다.
- BE 요구사항 판단이 필요하면 `$spec-read`로 최신성을 확인한다. 실패하면 요구사항 기반 결정을 중단한다.
- 하위 스킬이 요구하는 사용자 승인 게이트를 건너뛰지 않는다.
- `architecture-review` 결과 수정 사항이 있으면 `architecture-interview` 방식으로 질문, 추천안, 승인, 문서 보완을 다시 수행한다.
- 인터뷰 보완과 리뷰 반복은 최대 3회까지만 허용한다. 3회 후에도 차단 이슈가 남으면 확정하지 않고 중단한다.
- ADR, issue 분리, 심층 보안 리뷰, 운영 runbook 작성은 직접 수행하지 않고 후속 스킬 연계 항목으로 남긴다.
- 최종 fixed architecture가 통과한 뒤, 사용자 승인이 있으면 결정된 빌드/테스트/정적 분석/하네스 기준을 반영하기 위한 `package.json`, lockfile, Vite/Vitest/TypeScript/ESLint/Prettier/Playwright 설정, Git hook `.mjs`, CI 설정, 기본 `src`/test scaffold를 생성하거나 수정할 수 있다.
- 이 최종 구현 반영은 공통 FE 기반과 하네스 설정에만 한정한다. feature별 기능 구현, issue/ADR/TDD 산출물 작성은 수행하지 않는다.
- 원천 문서에 없는 값을 임의 확정하지 않는다.

## 먼저 확인할 자료

존재하는 파일만 읽는다.

- `AGENTS.md`
- `.codex/skills/architecture-interview/SKILL.md`
- `.codex/skills/architecture-review/SKILL.md`
- `.codex/skills/architecture-interview/references/document-templates.md`
- `.codex/skills/architecture-review/references/review-ledger-schema.md`
- `docs/design/*`
- `.cache/prd-read/docs/prd.md`, `docs/trd.md`, `.cache/prd-read/docs/features/*/prd.md`, `docs/features/*/trd.md`
- `docs/contracts/*`
- `docs/architecture/*`
- `package.json`, lockfile, `src`, `app`, `components`, `pages`, `routes`
- FE 설정, CI/CD, 배포, 하네스 관련 파일

## 실행 순서

1. 오늘 날짜를 로컬 기준 `yyyymmdd`로 정한다.
2. 기존 `docs/architecture/current-fixed.md`가 있으면 현재 적용 중인 fixed 디렉터리를 확인한다.
3. `$architecture-interview`를 실행해 필요한 아키텍처 결정을 질문하고 승인받아 문서화한다.
4. 인터뷰 과정과 답변을 `docs/architecture/interview-{yyyymmdd}/`에 기록한다.
5. `$architecture-review`를 실행해 인터뷰 산출물과 기존 문서, 코드, 설정 drift를 검토한다.
6. 리뷰에서 보완 사항이 없고 사용자 승인이 있으면 최종 fixed 문서를 작성한다.
7. 리뷰에서 보완 사항이 있으면 루프 카운트를 1 올리고, 보완 항목을 `$architecture-interview` 방식으로 다시 확정한다.
8. 보완한 문서를 다시 `$architecture-review`로 검토한다.
9. 루프 카운트가 3을 넘으면 더 반복하지 않고 `architecture-decision-blocked`로 보고한다.
10. 확정되면 `docs/architecture/fixed-{yyyymmdd}/`에 최종 문서를 작성하고 `docs/architecture/current-fixed.md`를 갱신한다.
11. 사용자가 승인한 경우 fixed architecture의 build/harness 결정을 실제 FE repo 설정에 반영한다. 예: `package.json`, lockfile, `vite.config.*`, `vitest.config.*`, `tsconfig*.json`, ESLint/Prettier/Playwright 설정, `.github`, hook/helper `.mjs`, 기본 `src`/test scaffold.
12. build/harness 설정 반영 후 가능한 범위에서 typecheck/lint/test/build 명령을 실행하고, 실패하면 fixed 문서는 유지하되 구현 반영 상태와 후속 조치를 보고한다.

## 반복 루프 규칙

- 1회차는 최초 인터뷰 후 리뷰다.
- 리뷰 보완이 발생하면 같은 날짜의 `interview-{yyyymmdd}/`에 `loop-{n}.md`로 질문, 답변, 보완 요약, 리뷰 결과를 남긴다.
- 각 루프는 다음 상태 중 하나로 끝난다.
  - `review-pass`: 보완 사항 없음
  - `review-needs-interview`: 사용자 결정이 필요한 보완 사항 있음
  - `review-blocked`: 요구사항, 코드, 계약, 문서 누락으로 진행 불가
- `review-needs-interview`는 최대 3회까지만 재진입한다.
- 3회 안에 `review-pass`가 나오지 않으면 fixed 문서를 만들지 않는다.

## 인터뷰 추적 문서

`docs/architecture/interview-{yyyymmdd}/`에는 다음 파일을 남긴다.

```text
docs/architecture/interview-{yyyymmdd}/
  summary.md
  loop-1.md
  loop-2.md
  loop-3.md
```

`summary.md`에는 다음을 기록한다.

- 실행 날짜
- 사용한 원천 문서
- 질문한 아키텍처 영역
- 사용자 답변과 채택된 추천안
- 리뷰 루프 횟수
- 각 루프의 상태
- 보완한 문서
- 최종 fixed 디렉터리 또는 차단 사유

각 `loop-{n}.md`에는 다음을 기록한다.

- 루프 번호
- 리뷰 지적 사항
- 다시 인터뷰한 질문
- 추천 답변과 사용자 승인 내용
- 반영한 문서
- 재리뷰 결과

## 최종 fixed 문서

모든 과정이 통과하면 `docs/architecture/fixed-{yyyymmdd}/`를 만들고 다음 문서를 작성한다.

```text
docs/architecture/fixed-{yyyymmdd}/
  impl-fixed.md
  infra-fixed.md
  harness-fixed.md
```

- `impl-fixed.md`: FE 구현 아키텍처, 런타임, 라우팅, 상태, API/STOMP client, 모듈/컴포넌트/스타일링 경계, TRD handoff 제약을 기록한다.
- `infra-fixed.md`: FE 서버/배포 인프라, hosting/CDN/reverse proxy, 환경 전략, 보안 헤더, 관측, sourcemap, 비용/용량 guardrail을 기록한다.
- `harness-fixed.md`: CI/CD, typecheck/lint/test/e2e, 정적 분석, Git hook mjs, contract drift, generated client/mock drift, dependency/supply-chain gate를 기록한다.

필요하면 각 fixed 문서와 같은 디렉터리에 Mermaid HTML 보조 문서를 둘 수 있다.

```text
docs/architecture/fixed-{yyyymmdd}/
  impl-diagram.html
  infra-diagram.html
  harness-diagram.html
```

Mermaid HTML은 이해 보조 자료일 뿐이며, 결정의 권위 원천은 `.md` 문서다.

## 현재 적용 fixed 포인터

확정이 끝나면 `docs/architecture/current-fixed.md`를 생성하거나 갱신한다.

```markdown
# Current Fixed Architecture

- active_fixed_dir: docs/architecture/fixed-{yyyymmdd}
- fixed_date: {yyyymmdd}
- impl: docs/architecture/fixed-{yyyymmdd}/impl-fixed.md
- infra: docs/architecture/fixed-{yyyymmdd}/infra-fixed.md
- harness: docs/architecture/fixed-{yyyymmdd}/harness-fixed.md
- interview_trace: docs/architecture/interview-{yyyymmdd}/summary.md
- review_ledger: docs/architecture/architecture-review-ledger.md
- status: fixed
```

다른 스킬은 현재 적용 중인 아키텍처 기준이 필요하면 먼저 `docs/architecture/current-fixed.md`를 읽고, 그 안의 `active_fixed_dir`을 따른다.

## 완료 조건

- `architecture-interview`의 승인된 결정이 문서화되어 있다.
- `architecture-review`가 보완 사항 없음 또는 승인된 보완 반영 완료로 끝났다.
- 리뷰 보완 루프가 3회를 넘지 않았다.
- `docs/architecture/interview-{yyyymmdd}/summary.md`에 과정이 남아 있다.
- `docs/architecture/fixed-{yyyymmdd}/impl-fixed.md`, `infra-fixed.md`, `harness-fixed.md`가 존재한다.
- `docs/architecture/current-fixed.md`가 최신 fixed 디렉터리를 가리킨다.
- 남은 미확정, 상위 산출물 재검토, 후속 스킬 연계 항목이 보고되어 있다.
- build/harness 설정을 반영한 경우, 수정한 설정 파일과 실행한 검증 명령이 보고되어 있다.

## 완료 보고

작업을 마치면 다음만 간결히 보고한다.

- 최종 상태: `architecture-decision-fixed`, `architecture-decision-blocked`, `architecture-decision-review-loop-exhausted`
- 리뷰 루프 횟수
- 생성 또는 갱신한 `interview-{yyyymmdd}` 문서
- 생성 또는 갱신한 `fixed-{yyyymmdd}` 문서
- 갱신한 `current-fixed.md`
- Mermaid HTML 생성 여부
- build/harness 설정 수정 여부와 수정 파일
- 실행한 검증 명령과 결과
- 남은 미확정 사항과 후속 스킬 연계 항목
