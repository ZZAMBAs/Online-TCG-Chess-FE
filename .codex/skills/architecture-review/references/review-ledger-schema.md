# Architecture Review Ledger Schema

`architecture-review-ledger.md`는 변경 없는 FE 아키텍처 영역을 안전하게 생략하기 위한 기록이다.

## 권장 섹션

```markdown
# Architecture Review Ledger

## 목적

## 리뷰 영역 요약

| area | last_reviewed_at | decision_summary | skipped_this_run | skip_reason |
| --- | --- | --- | --- | --- |

## 영역별 상세

### {area}

- last_reviewed_at:
- source_documents:
- watched_paths:
- ignored_paths:
- contract_sources:
- ci_checks:
- source_fingerprint:
- implementation_paths:
- implementation_fingerprint:
- decision_summary:
- skip_conditions:
- re_review_triggers:
- latest_result:
```

## area 후보

- frontend-runtime-build-tool
- typescript-configuration
- routing-boundary
- state-management-server-cache
- api-client-error-auth
- stomp-websocket-client
- module-import-boundaries
- component-architecture
- styling-design-system-boundary
- frontend-hosting-cdn-proxy
- environment-runtime-config
- security-headers-public-secret
- client-observability-sourcemap
- cicd
- git-hook-mjs-harness
- static-analysis-lint
- test-strategy-quality-gates
- contract-drift-gates
- generated-client-mock-drift
- be-contract-collaboration
- dependency-supply-chain-policy
- release-preview-stage-prod

## 생략 조건 작성 기준

생략 조건은 구체적인 path와 결정 요약을 포함한다. "변경 없음"처럼 막연하게 쓰지 않는다.

## path mapping 작성 기준

- `watched_paths`에는 해당 area가 재검토되어야 하는 원천 문서, 코드, 설정 경로를 적는다.
- `ignored_paths`에는 `node_modules`, `dist`, `coverage`, screenshot, test artifact, generated output처럼 fingerprint에서 제외할 경로를 적는다.
- `contract_sources`에는 OpenAPI, STOMP schema, BE spec/PRD hash, generated client source 같은 계약 원천을 적는다.
- `ci_checks`에는 해당 area를 검증하는 CI job 또는 npm script 이름을 적는다.

## 재검토 조건 작성 기준

다음 변화는 반드시 재검토 조건에 포함한다.

- 관련 요구사항 변경
- 관련 PRD/TRD/storyboard 또는 인터페이스 계약 변경
- 관련 FE 코드 또는 설정 변경
- package manager, lockfile, dependency, engine 정책 변경
- 라우팅, 상태 관리, API client, STOMP client, 모듈 경계, 스타일링 방식 변경
- CI/CD 또는 배포/인프라 설정 변경
- security header, public env, secret 처리 변경
- typecheck/lint/test/e2e/contract drift required check 변경
- OpenAPI/STOMP schema source, generated client, MSW mock, breaking change 절차 변경
- Git hook mjs guard 또는 lint-staged 정책 변경
- 미확정 항목 확정
