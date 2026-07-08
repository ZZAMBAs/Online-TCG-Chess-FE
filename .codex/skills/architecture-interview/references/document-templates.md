# Architecture Document Templates

이 문서는 `architecture-interview`가 승인된 FE 아키텍처 결정을 문서화할 때 사용하는 템플릿이다.

## frontend-architecture.md

```markdown
# Frontend Architecture

## 목적
## 원천 산출물
## 현재 구현 기준 또는 후보 기준
## FE 런타임과 빌드 도구
## TypeScript 정책
## 라우팅과 라우트 경계
## 상태 관리와 서버 캐시
## API Client와 오류/Auth 처리
## BE Contract Collaboration
## Generated Client와 Mock 동기화
## STOMP/WebSocket Client
## 모듈 경계와 import 규칙
## 컴포넌트 경계
## 스타일링과 디자인 시스템 경계
## 디자이너 협업과 Handoff
## Breakpoint와 Responsive 기준
## Accessibility Baseline
## Storybook 또는 Component Catalog
## Storyboard-to-Component Traceability
## 공통 에러/로딩/empty/permission UX
## 정적 분석과 강제 규칙
## 테스트와 품질 게이트
## 미확정 사항
```

## frontend-infrastructure.md

```markdown
# Frontend Infrastructure

## 목적
## 원천 산출물
## MVP FE 인프라 전제
## 배포 형태
## FE/BE 배포 관계
## CDN, Reverse Proxy, Edge
## 정적 자산과 캐시 정책
## Environment Strategy
## Runtime Config와 공개 변수
## Secret 노출 방지
## Security Headers
## Client Observability
## Sourcemap와 Release Version
## Capacity/Cost Guardrail
## MVP 제외 확장 후보
## 후속 스킬 연계
## 미확정 사항
```

## cicd-architecture.md

```markdown
# CI/CD Architecture

## 목적
## 원천 산출물
## 브랜치와 머지 정책
## Package Manager와 Lockfile 정책
## Required Checks
## Typecheck
## Lint와 Format
## Unit/Component Test
## E2E Test
## Build 검증
## Contract Drift Check
## Generated Client 검증
## MSW Mock Drift 검증
## Dependency와 Supply-chain 검사
## 테스트 리포트와 메트릭 검사
## Preview/Stage/Prod 배포
## Release Gates
## Artifact와 Version
## Rollback 정책
## Secret 처리
## 후속 스킬 연계
## 미확정 사항
```

## deployment-view.md

```markdown
# Deployment View

## 목적
## 전체 FE 배포 Topology
## FE/BE 네트워크 경계
## Hosting/CDN/Reverse Proxy 구성
## 환경별 차이
## Runtime Config 주입
## 정적 자산 흐름
## Client Observability 흐름
```

## harness-guardrails.md

```markdown
# Harness Guardrails

## 목적
## Hard Gate
## Conditional Gate
## Advisory 도구
## TypeScript 강제 규칙
## ESLint와 Import Boundary
## Formatting과 Style Guard
## Git Hook mjs Guard
## MJS Guard 입력/출력/Fixture 정책
## Unit/Component Test Guard
## E2E Guard
## Contract Drift Guard
## Dependency와 Supply-chain Guard
## CI Required Check
## 테스트 실행 리포트와 메트릭
## Artifact 보존과 정리 정책
## 도입 전 PoC 항목
## 후속 스킬 연계
## 미확정 사항
```

## create-trd-handoff.md

```markdown
# Create TRD Handoff

## 목적
## 원천 산출물과 입력 버전
## 확정된 FE Architecture Constraints
## TRD 필수 준수 Gate
## BE 계약 의존성
## Storyboard Traceability
## 미확정 질문과 소유자
## 상위 산출물 재검토 필요
## TRD에서 재결정 금지 항목
## TRD에서 기능별 구체화할 항목
```

## architecture-traceability.md

```markdown
# Architecture Traceability

| 결정 | 출처 산출물 | 출처 섹션 | 반영 문서 | 상태 |
| --- | --- | --- | --- | --- |
```

## architecture-review-ledger.md

`architecture-review`의 `references/review-ledger-schema.md` 형식을 따른다.
