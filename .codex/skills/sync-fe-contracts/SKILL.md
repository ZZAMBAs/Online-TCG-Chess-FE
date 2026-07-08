---
name: sync-fe-contracts
description: Online-TCG-Chess-FE에서 BE repo의 docs/negotiation/{topic}/summarize.md 중 fixed 상태인 FE/BE 계약을 읽고 FE 구현 참조용 docs/contracts/{topic}.md로 필요한 내용만 투영해야 할 때 사용한다. BE 협상 결과를 FE repo docs에 반영하되, 구현 계획, 테스트 설계, 이슈 분리, TDD RED/GREEN/BLUE, 리팩터링, mock/MSW 전략, contract drift gate 설계는 하지 않는다.
---

# Sync FE Contracts

## 개요

BE 협상 결과의 권위 원천을 FE 구현 참조 문서로 투영한다. 이 스킬은 계약 소비 문서만 만들며, FE 아키텍처 결정이나 기능 이슈/TDD 워크플로우를 대신하지 않는다.

## 기본 원칙

- 모든 분석과 문서는 한국어로 작성한다.
- BE 저장소 기준은 `https://github.com/ZZAMBAs/Online-TCG-Chess-BE`로 둔다.
- FE 저장소 기준은 `https://github.com/ZZAMBAs/Online-TCG-Chess-FE`로 둔다.
- 권위 원천은 BE repo의 `docs/negotiation/{topic}/summarize.md`다.
- FE 출력 문서는 권위 계약 원본이 아니라 FE 구현 참조 projection이다.
- BE 요구사항 원문, BE 협상 전문, BE 내부 구현 세부를 FE repo에 복사하지 않는다.
- BE summary의 `status: fixed`만 FE 문서로 투영한다.
- `proposed`, `in_review`, `needs_user_decision` 상태는 FE 계약 문서로 만들지 않는다.
- FE 앱 코드, storyboard, BE repo 문서는 수정하지 않는다.
- API client 구조, STOMP client 구조, state management 방식, generated client/MSW/mock 정책, contract drift gate 설계는 작성하지 않는다. 해당 내용은 `architecture-interview` 또는 `architecture-review` 책임이다.
- AC, Given-When-Then, 이슈 분리, ADR, TDD RED/GREEN/BLUE, 테스트 케이스, 리팩터링 계획은 작성하지 않는다. 해당 내용은 후속 FE issue/TDD workflow 스킬 책임이다.

## 입력 확인

먼저 존재하는 자료만 읽는다.

- BE 협상 결과: BE repo의 `docs/negotiation/{topic}/summarize.md`
- FE 기존 계약 projection: `docs/contracts/*.md`
- FE 아키텍처 산출물: `docs/architecture/*`
- FE 요구사항 동기화 지침: `AGENTS.md`, `.codex/skills/spec-read/SKILL.md`

BE local checkout은 사용자 또는 호출자가 제공한 경로를 우선 사용한다. 제공 경로가 없으면 FE repo sibling 경로에서 `Online-TCG-Chess-BE`를 찾고, 가능하면 remote가 `https://github.com/ZZAMBAs/Online-TCG-Chess-BE`와 맞는지 확인한다.

BE summary를 찾을 수 없거나 source repo 확인이 실패하면 새 FE 계약 문서를 만들지 말고 중단 사유를 보고한다.

BE 요구사항 판단이 필요하면 `$spec-read`로 최신성을 확인한다. 원격 최신성 확인 실패 시 캐시 기준으로 추정하지 않는다.

## 대상 선택

사용자가 topic을 지정하면 해당 topic만 처리한다.

사용자가 topic을 지정하지 않으면 BE repo의 `docs/negotiation/*/summarize.md`를 탐색해 `status: fixed`인 topic만 후보로 삼는다. 이미 동일 source path와 source commit/hash로 FE 문서가 존재하면 건너뛸 수 있다.

topic 이름은 BE negotiation 디렉터리명을 그대로 사용한다. 출력 파일은 `docs/contracts/{topic}.md`다.

## 출력 구조

FE repo에는 다음 구조만 생성하거나 갱신한다.

```text
docs/contracts/
  {topic}.md
```

`docs/contracts/index.md`는 만들지 않는다.

`docs/contracts/{topic}.md`는 다음 섹션을 사용한다.

```markdown
# {Topic} FE Contract

## Source

- source_repo:
- source_path:
- source_status:
- source_commit:
- source_verification:

## Status

## FE-Relevant Contract

## FE Consumption Notes

## Excluded From FE Projection
```

## 내용 추출 규칙

BE `summarize.md`에서 다음만 추린다.

- `## 결정` 중 FE가 직접 소비해야 하는 계약
- `## FE 구현 영향` 중 구현 참조에 필요한 사실
- `## 참조 메모 반영 대상` 중 FE 문서 반영 대상

다음은 제외하고, 필요하면 `Excluded From FE Projection`에 제외 사유만 남긴다.

- BE 내부 구현 영향
- 서버 트랜잭션, persistence, repository, domain implementation 세부
- 테스트 설계, mock/MSW 전략, fixture 생성 방식
- 이슈/ADR 후보, AC, Given-When-Then, TDD 단계
- 리팩터링 계획 또는 구현 순서
- BE 요구사항 원문 또는 협상 전문

FE가 임의 해석한 내용은 확정 계약처럼 쓰지 말고 `FE Consumption Notes`에 "FE 해석"으로 표시한다. 확인이 필요한 항목은 새 문서를 만들기보다 작업을 중단하고 사용자 또는 BE 협상 재개 필요로 보고한다.

## Source 기록 규칙

- `source_repo`는 `https://github.com/ZZAMBAs/Online-TCG-Chess-BE`로 기록한다.
- `source_path`는 `docs/negotiation/{topic}/summarize.md`로 기록한다.
- `source_status`는 BE summary의 상태를 그대로 기록한다.
- `source_commit`은 가능하면 BE repo의 현재 commit hash를 기록한다.
- commit/hash 확인이 불가능하면 `source_verification: unavailable`로 기록하고 `Status`에 확인 필요성을 남긴다.

`status: fixed`가 아닌 source는 문서를 만들지 않는 것이 기본이다. 이미 같은 topic 문서가 있더라도 source가 fixed가 아니면 갱신하지 말고 상태 불일치를 보고한다.

## 기존 문서 갱신

기존 `docs/contracts/{topic}.md`가 있으면 다음을 확인한다.

- source path가 같은가
- source commit/hash 또는 source 내용이 바뀌었는가
- 기존 문서에 구현 계획, 테스트 설계, 이슈/TDD 내용이 섞였는가

source가 바뀌었으면 기존 문서를 갱신한다. 이때 FE에서 손으로 추가한 구현 계획이나 테스트 계획은 보존하지 말고 제거 대상이라고 보고한다. 이 스킬의 출력은 계약 projection만 유지한다.

## 완료 보고

작업을 마치면 다음만 간결히 보고한다.

- 처리한 topic
- 생성 또는 갱신한 `docs/contracts/{topic}.md`
- 사용한 BE source path와 commit/hash 확인 여부
- 건너뛴 topic과 사유
- 후속으로 넘길 항목: 아키텍처 검토 필요, issue/TDD 워크플로우 필요, BE 협상 재개 필요
