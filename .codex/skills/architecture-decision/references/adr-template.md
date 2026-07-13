# Architecture ADR Template

아키텍처 ADR은 FE 전역 구조, 런타임, 상태·통신 경계, 인프라, CI/CD, 정적 분석과 하네스 선택의 근거를 보존한다. feature 구현 ADR이나 issue/AC/TDD 계획은 포함하지 않는다.

## 파일 경로

```text
docs/architecture/adr/adr-{nnn}-{slug}.md
```

`{nnn}`은 아키텍처 ADR 전체에서 증가하는 세 자리 번호이며, slug는 소문자 ASCII kebab-case다.

## Frontmatter

```yaml
---
id: "ARCH-ADR-{nnn}"
status: "proposed"
decision_scope: "frontend-architecture | infrastructure | ci-cd | harness"
fixed_reference: "없음"
supersedes: []
source_documents:
  - "docs/architecture/interview-{yyyymmdd}/summary.md"
---
```

- `status`는 `proposed`, `accepted`, `superseded`, `deferred` 중 하나다.
- 확정 뒤 `fixed_reference`에 관련 `fixed-{yyyymmdd}` 문서를 기록한다.
- 새 ADR이 기존 결정을 바꾸면 새 ADR의 `supersedes`와 이전 ADR의 상태·대체 ADR을 함께 갱신한다.

## 본문 형식

본문 기본 섹션은 다음 네 개만 사용한다.

```markdown
# ARCH-ADR-{nnn}. {결정 제목}

## Context

결정 배경, 요구사항·디자인 기준·기존 FE 구현·운영/비용/보안/검증 제약과 지금 결정하지 않을 때의 위험을 적는다.

## Decision

선택한 대안과 이유를 현재 프로젝트 범위, 기존 구현, 배포·운영 부담, 비용, 보안과 검증 가능성에 연결해 적는다.

## Alternatives

| 대안 | 장점 | 단점/위험 | 현재 상황에서의 적합성 | 선택 또는 제외 이유 |
| --- | --- | --- | --- | --- |
| {대안 A} | {장점} | {단점/위험} | {현재 요구사항·디자인·구현·운영 제약과의 연결} | {선택 또는 제외 이유} |
| {대안 B} | {장점} | {단점/위험} | {현재 요구사항·디자인·구현·운영 제약과의 연결} | {선택 또는 제외 이유} |

## Consequences

긍정적 영향, 수용한 trade-off, 선택하지 않은 대안 대비 잃는 점, fixed 문서·후속 작업 반영 사항과 재검토 조건을 적는다.
```

선택하지 않은 이유를 `복잡함`, `불필요함`처럼 근거 없이 단정하지 않는다. 실질적인 대안이 없거나 요구사항이 이미 결론을 강제한 단순 구현 메모는 ADR로 승격하지 않는다.
