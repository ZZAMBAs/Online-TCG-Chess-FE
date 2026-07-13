---
name: architecture-interview
description: Online-TCG-Chess-FE에서 FE 구현 아키텍처, FE 서버/배포 인프라, CI/CD, 정적 분석, Git hook mjs 하네스, 테스트/계약 드리프트 게이트를 한국어 인터뷰로 확정하고 승인 후 docs/architecture 문서로 생성·갱신해야 할 때 사용한다. 기존 spec/prd/trd/storyboard/architecture 산출물과 현재 FE 코드·설정을 읽고, FE 아키텍처 선택지를 직접 도출해 한 번에 하나씩 질문과 추천안을 제시해야 할 때 사용한다.
---

# Architecture Interview

## 개요

FE 구현 아키텍처, FE 서버/배포 인프라, CI/CD, 정적 분석과 AI 하네스 품질 게이트 결정을 한국어 인터뷰로 구체화하고, 승인된 결정은 `docs/architecture/` 문서로 생성하거나 갱신한다. PRD/TRD가 다룰 기능별 상세 설계를 다시 묻지 않고, FE 전체 개발 기준과 하네스를 결정한다.

## 기본 원칙

- 모든 질문과 요약은 한국어로 작성한다.
- 질문은 반드시 한 번에 하나만 한다.
- 질문은 충분하다고 판단될 때까지 계속한다.
- 이미 확정된 결정은 다시 묻지 않는다. 기존 산출물, 현재 코드, 새 답변이 충돌하면 확인 질문을 한다.
- 기존 스킬 산출물이 있으면 반드시 먼저 읽고 재사용한다.
- BE 요구사항 판단이 필요하면 `$spec-read`로 최신성을 확인한다. 실패하면 요구사항 기반 결정을 중단한다.
- `docs/design/design-baseline.md`가 없거나 `approved`가 아니면 디자인 시스템·스타일링 경계 질문을 진행하지 않고 `$design-decision`을 먼저 요청한다.
- 현재 FE 구현 코드와 설정을 확인해 질문 범위를 확장하거나 축소한다.
- 아직 구현되지 않은 영역은 아키텍처 후보로 다루고, 이미 구현된 영역은 문서와 코드 drift를 확인한다.
- 기능 상세, API payload 필드, 화면 문구, 세부 UX, 상세 스타일값처럼 storyboard/TRD에서 다룰 사항은 아키텍처 질문으로 확정하지 않는다.
- 질문 은행 파일에 의존하지 않는다. 읽은 산출물과 현재 코드에서 필요한 FE 아키텍처 질문을 직접 생성한다.
- 오케스트레이션 중 아키텍처 ADR로 승격할 수 있도록 각 결정의 실제 대안, 채택·제외 이유, trade-off, 재검토 조건을 수집한다. ADR 파일과 상태·인덱스 관리는 `$architecture-decision`이 소유한다.
- issue 분리, feature 구현 ADR, 심층 보안 리뷰, 운영 runbook 작성은 이 스킬에서 수행하지 않고 후속 스킬 연계 항목으로 남긴다.
- 요구사항 변경이 필요하면 직접 수정하지 않고 `상위 산출물 재검토 필요`로 기록한다.
- 파일 작성 전에는 반영 예정 요약을 세션에 제시하고 승인받는다.
- 개별 스킬 내부에 전체 워크플로우 순서를 강제하지 않는다.

## 먼저 확인할 자료

존재하는 파일만 읽는다.

- `AGENTS.md`
- `docs/design/storyboard-manifest.json`, `docs/design/storyboard-pages.md`, `docs/design/storyboard/fragments/*`
- `.cache/prd-read/docs/prd.md`, `docs/trd.md`, `docs/websocket-spec.md`
- `.cache/prd-read/docs/features/*/prd.md`, `docs/features/*/trd.md`
- `docs/architecture/*`
- `package.json`, lockfile, `src`, `app`, `components`, `pages`, `routes`
- `vite.config.*`, `next.config.*`, `nuxt.config.*`, `tsconfig*.json`
- `eslint.config.*`, `.eslintrc*`, `prettier.config.*`, `.prettierrc*`
- `tailwind.config.*`, `postcss.config.*`, style/theme/token files
- `vitest.config.*`, `playwright.config.*`, `cypress.config.*`
- `.husky`, `.lintstagedrc*`, hook/helper `.mjs` files
- `.github`, `Dockerfile`, `docker-compose*`, `infra`, `deploy`, hosting config

## 질문 방식

각 질문은 다음 형식을 유지한다.

```markdown
질문: [하나의 구체적인 FE 아키텍처 결정 질문]

추천 답변: [현재 프로젝트 맥락에서 권장하는 선택]

추천 이유: [FE 구현/배포/품질/하네스 관점의 근거]

대안: [2-4개 선택지와 각각의 핵심 장단점]

ADR 후보: [예/아니오와 판단 이유]

영향받는 문서: [예: frontend-architecture.md, harness-guardrails.md]

상위 산출물 재검토 필요: [없음 또는 spec/prd/trd/storyboard 중 필요한 항목과 이유]
```

사용자가 "추천대로", "계속", "알아서"처럼 위임하면 추천 답변을 채택하고 다음 질문으로 넘어간다.

답변을 채택할 때는 채택한 안만 남기지 말고 실제 제시한 대안, 채택하지 않은 이유, 수용한 trade-off와 재검토 조건을 인터뷰 추적 자료에 함께 보존한다. 실질적 대안이 없거나 요구사항이 결론을 강제한 항목은 `ADR 후보: 아니오`로 표시한다.

## 질문 생성 범위

자료를 읽은 뒤 다음 범위에서 필요한 질문을 직접 생성한다. 각 질문은 선택지를 2-4개로 좁히고, 현재 프로젝트 기준 추천안을 함께 제시한다.

### FE 구현 아키텍처

- 앱 런타임과 빌드 도구: React/Vue, Vite/Next/Nuxt, SPA/SSR/SSG 중 무엇을 채택할지 묻는다.
- TypeScript 정책: strict, noUncheckedIndexedAccess, exactOptionalPropertyTypes, path alias, generated type 취급을 묻는다.
- 라우팅 구조: file-based/router config, route guard, auth boundary, lazy loading, error boundary 위치를 묻는다.
- 상태 관리: page state, server cache, global client state, derived state, optimistic update 허용 범위를 묻는다.
- API client 구조: fetch/axios, OpenAPI client, error mapping, auth refresh, retry/timeout, contract drift 대응을 묻는다.
- STOMP/WebSocket client 구조: connection owner, subscription lifecycle, reconnect/backoff, message validation, REST와 동기화 전략을 묻는다.
- 모듈 경계: feature-sliced, domain-driven frontend, route-based, shared UI/core/data 계층과 import 금지 방향을 묻는다.
- 컴포넌트 경계: page/container/presentational, form, modal/sheet, board/card UI, provider 배치를 묻는다.
- 스타일링 방식: CSS Modules, Tailwind, styled-components/emotion, design token, Storybook 도입 여부를 묻는다.
- 에러/로딩/empty/permission UX의 공통 처리 위치를 묻는다.
- `create-trd`가 따라야 할 아키텍처 제약, hard gate, 미확정 질문, storyboard 영향, BE 계약 의존성을 어떻게 전달할지 묻는다.

### 디자이너 협업과 디자인 시스템

- Git 디자인 기준, storyboard, 코드, Figma 같은 외부 도구 중 디자인 source of truth를 어디에 둘지 묻는다. 외부 도구가 없다는 이유로 진행을 막지 않는다.
- design token의 소유자, 저장 위치, naming, FE 적용 방식, token 우회 금지 기준을 묻는다.
- responsive breakpoint, density, spacing scale, typography scale을 누가 확정하고 어디에 기록할지 묻는다.
- Storybook 또는 동등한 컴포넌트 카탈로그를 도입할지와 designer handoff에 사용할 범위를 묻는다.
- component acceptance checklist를 묻는다. 예: 상태 variant, loading/error/empty/disabled, keyboard, focus, a11y, mobile.
- visual regression 또는 visual smoke gate를 도입할지와 artifact 보존/삭제 정책을 묻는다.
- storyboard page id와 실제 route/component/story id의 traceability를 어떻게 남길지 묻는다.
- 승인된 디자인 기준의 실제 token 값이나 primitive 시각값은 다시 결정하지 않고, 구현 기술·저장 위치·component boundary·검증 gate로만 번역한다.
- a11y baseline을 묻는다. 예: semantic HTML, aria, contrast, keyboard navigation, axe 검사, Playwright a11y smoke.

### FE 서버와 배포 인프라

- 배포 형태: 정적 호스팅, CDN, Node SSR server, edge runtime, reverse proxy 연계를 묻는다.
- FE/BE 배포 관계: same-site, subdomain, path-based reverse proxy, CORS, cookie SameSite 제약을 묻는다.
- 환경 전략: local/dev/stage/prod, preview env, `.env` 공개 변수 prefix, runtime config, config drift 방지를 묻는다.
- 정적 자산: CDN cache policy, asset hashing, image/font handling, object storage 연계 후보를 묻는다.
- 보안 헤더: CSP, HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy 적용 위치를 묻는다.
- 관측: client error reporting, web vitals, console/error hygiene, release version tagging, sourcemap 공개 범위를 묻는다.
- capacity/cost guardrail: managed hosting, CDN, SSR server 비용과 MVP 제외/전환 조건을 묻는다.
- 보안 헤더, runtime config, CDN/proxy 설정이 어느 계층과 파일에서 소유되는지 묻는다.

### CI/CD와 AI 하네스

- required checks: typecheck, lint, unit test, e2e, build, dependency audit, contract drift check를 묻는다.
- 정적 분석: type-aware ESLint, dependency-cruiser, Knip/ts-prune, depcheck, Stylelint 도입 여부와 실패 조건을 묻는다.
- 포맷/품질: Prettier, import sorting, no inline style, design token 우회 금지, accessibility lint 범위를 묻는다.
- Git hook mjs 하네스: pre-commit/pre-push에서 실행할 Node `.mjs` guard, lint-staged, 변경 범위 검사, 금지 패턴 검사를 묻는다.
- 테스트: Vitest, Testing Library, MSW, Playwright, visual smoke, e2e artifact 보존과 실패 조건을 묻는다.
- 계약 드리프트: OpenAPI/STOMP schema, BE PRD/spec hash, generated client, mock data drift를 어떻게 검증할지 묻는다.
- BE 협업 프로토콜: contract source, generated client 갱신 명령, MSW mock 생성/검증, STOMP message schema 검증, breaking change 처리 절차를 묻는다.
- 공급망: npm audit, lockfile policy, dependency review, package manager, engine pinning, dependency approval 방식을 묻는다.
- 테스트 실행 메트릭: 실행 시간, 실패율, flaky test, skipped test, retry 여부, artifact 보존을 묻는다.

## TRD로 넘길 항목

다음은 아키텍처 인터뷰에서 확정하지 말고 TRD 또는 상위 산출물 재검토 대상으로 표시한다.

- 사용자 기능 포함/제외 범위
- 상세 API endpoint, payload, 필드명
- feature별 상태 머신 상세
- 화면 문구, UI layout 세부 UX, 세부 스타일값
- 오류 코드의 개별 명칭과 상세 메시지
- feature별 테스트 케이스의 구체 입력값
- 카드 효과, 체스 규칙, MMR 공식 등 도메인 정책값

## create-trd handoff

아키텍처 문서화가 끝나면 `create-trd`가 그대로 읽을 수 있도록 다음 항목을 `create-trd-handoff.md` 또는 `architecture-traceability.md`에 남긴다.

- 확정된 FE architecture constraints
- 기능별 TRD가 반드시 따라야 할 Hard/Conditional/Advisory gate
- 미확정 질문과 질문 소유자
- 상위 산출물 재검토 필요 항목
- BE 계약 의존성: OpenAPI/STOMP/schema/spec hash/source 문서
- storyboard 영향: 관련 page id, parent_id, entry_points, PC/Mobile 차이
- TRD에서 재결정하면 안 되는 공통 FE 정책
- TRD에서 기능별로 구체화해야 하는 항목

## 후속 스킬로 넘길 항목

- issue/ADR 스킬: feature 구현 ADR과 구현 issue 분리. FE 전역 아키텍처 ADR은 `$architecture-decision`이 직접 소유한다.
- security-review 스킬: threat modeling, XSS/CSRF/token storage/privacy abuse case 상세
- documentation/runbook 스킬: 운영 runbook, 배포/롤백 절차, 온보딩 문서, 릴리즈 노트
- spec/storyboard 재검토: 화면 흐름, 권한 상태, 오류 상태, 트래픽 목표, SLO/SLA 같은 요구사항 성격 결정

## AI 하네스 질문 필수 조건

FE 아키텍처를 논의할 때는 다음 도구 또는 동등한 대안을 적용할지 반드시 질문한다.

- TypeScript strict와 추가 strict 옵션
- type-aware ESLint
- Prettier와 import sorting
- dependency-cruiser 또는 import boundary checker
- Knip/ts-prune/depcheck 계열 unused export/dependency 검사
- Stylelint 또는 스타일 금지 패턴 검사
- Git hook용 `.mjs` guard script
- Vitest와 Testing Library
- MSW 또는 API mock strategy
- Playwright e2e와 artifact 정리 정책
- OpenAPI/STOMP/BE spec hash 기반 contract drift check
- generated client와 MSW mock 동기화 검증
- STOMP message schema 검증과 breaking change 처리 절차
- npm audit, lockfile policy, engine/package manager pinning
- CI test report, coverage report, e2e artifact 보존 및 실패 조건

각 도구는 `Hard gate`, `Conditional gate`, `Advisory` 중 하나로 분류하고, CI에서 실패시킬 수 있는지 확인한다.

## Git hook mjs 하네스

- Git hook 또는 CI에서 재사용할 `.mjs` guard를 설계할 때는 `references/mjs-harness-template.md`를 읽고 따른다.
- guard는 hook 전용 임시 스크립트가 아니라 CI에서도 같은 규칙을 실행할 수 있게 설계한다.

## 생성 또는 갱신할 문서

승인된 결정은 다음 구조로 문서화한다. 상세 섹션은 `references/document-templates.md`를 읽고 따른다.

```text
docs/architecture/
  frontend-architecture.md
  frontend-infrastructure.md
  cicd-architecture.md
  deployment-view.md
  harness-guardrails.md
  create-trd-handoff.md
  architecture-traceability.md
  architecture-review-ledger.md
```

## 문서 작성 규칙

- 확정된 결정과 문서화 가정을 구분한다.
- 원천 문서에 없는 값을 임의 확정하지 않는다.
- 확정되지 않은 항목은 `미확정` 또는 `아키텍처 후보`로 표시한다.
- 기존 아키텍처 문서가 있으면 먼저 읽고 갱신한다.
- 문서와 구현이 충돌하면 drift로 기록한다.
- 실제 FE 앱 소스가 없으면 구현 기준이 아니라 후보 기준으로 기록한다.
- CI에서 실패시킬 수 있는 하드 게이트와 보조 도구를 구분한다.
- release readiness와 operational readiness 중 CI에서 실패 조건화할 수 있는 항목은 하네스 문서에 포함한다.
- 아키텍처 ADR 후보와 대안 비교는 인터뷰 추적 자료에 기록하고 `$architecture-decision`에 넘긴다. feature 구현 ADR, 심층 보안 리뷰, runbook은 후속 스킬 연계 항목으로 기록한다.

## 문서 반영 전 요약

충분한 답변이 모이면 파일을 쓰기 전에 다음을 세션에서 요약하고 명확한 승인을 받는다.

- 확정된 FE 구현 아키텍처 결정
- 확정된 FE 서버/배포 인프라 결정
- 확정된 CI/CD 결정
- 확정된 AI 하네스/정적 분석/Git hook 결정
- 아키텍처 ADR 후보별 채택안, 제외 대안, 제외 이유, 재검토 조건
- 미확정 사항
- 상위 산출물 재검토 필요 항목
- 후속 스킬 연계 필요 항목
- 생성 또는 갱신할 아키텍처 문서
