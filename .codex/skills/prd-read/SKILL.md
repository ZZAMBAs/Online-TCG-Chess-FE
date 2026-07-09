---
name: prd-read
description: Online-TCG-Chess-FE에서 BE가 생성한 전체 PRD와 기능별 PRD 원천을 확인, 분석, 구현 계획, 이슈 분리, TRD/스토리보드/아키텍처 판단에 사용한다. BE 저장소 master의 docs/prd.md, docs/features/{feature}/prd.md, docs/traceability.md를 원격 최신성 확인 후 .cache/prd-read에 캐시하고 FE docs 동일 경로에 projection하며, 원격 확인 실패 시 캐시가 있어도 PRD 기반 작업을 중단한다.
---

# PRD Read

## 원칙

- BE PRD 원천은 `ZZAMBAs/Online-TCG-Chess-BE`의 `master` 브랜치 PRD 산출물이다.
- 원천 경로는 BE `create-prd` 스킬 기준인 `docs/prd.md`, `docs/features/{feature}/prd.md`, 선택적 `docs/traceability.md`다.
- FE 저장소의 `docs/prd.md`, `docs/features/{feature}/prd.md`, `docs/traceability.md`는 BE PRD 원천의 FE-local projection이다. 권위 원천은 항상 BE repo이며, FE projection을 손으로 고치지 않는다.
- PRD 기반 답변, 구현 계획, 이슈 분리, TRD/스토리보드/아키텍처 판단 전에는 원격 최신성을 먼저 확인한다.
- 원격 최신성 확인에 실패하면 캐시가 있어도 사용하지 않는다.
- BE 저장소에 PRD 산출물이 아직 없으면 "원천 PRD 없음"으로 보고하고 PRD 기반 작업을 중단한다.
- BE 요구사항 원문 자체가 필요하면 이 스킬이 아니라 `$spec-read`를 사용한다.

## 기본 절차

1. 저장소 루트에서 helper를 실행한다.

   ```bash
   python3 .codex/skills/prd-read/scripts/read_be_prd.py
   ```

2. 특정 기능 PRD만 필요하면 feature 이름을 명시한다.

   ```bash
   python3 .codex/skills/prd-read/scripts/read_be_prd.py --feature matchmaking
   ```

3. helper가 성공하면 출력된 manifest, 캐시 파일, FE projection 파일을 읽어 PRD를 분석한다.
4. helper가 실패하면 캐시를 열지 말고 작업을 중단한다.
5. REST/STOMP처럼 외부 노출 계약을 다루면, PRD 확인 후 `$spec-read`와 contract freeze 여부도 확인한다.

## Helper 동작

- 먼저 원격 `master` HEAD를 확인해 캐시가 최신인지 판단한다.
- 캐시가 최신이면 `.cache/prd-read/docs/`와 `.cache/prd-read/manifest.json`을 재사용하고, 같은 내용을 FE repo `docs/` 동일 경로에 다시 projection한다.
- 원격 HEAD가 바뀌었거나 캐시가 없으면 BE PRD 산출물을 다시 받는다.
- 새로 받은 PRD 산출물은 `.cache/prd-read/docs/`에 캐시한 뒤 `docs/prd.md`, `docs/features/{feature}/prd.md`, `docs/traceability.md`에 projection한다.
- PRD 조회 순서는 GitHub tree API와 raw URL, `gh api`, `.cache/prd-read/be-repo` shallow clone 재사용 순서다.
- 수집 대상은 정확히 다음 경로만이다.
  - `docs/prd.md`
  - `docs/features/*/prd.md`
  - `docs/traceability.md`
- feature 인자가 있으면 `docs/features/{feature}/prd.md`가 정확히 있어야 한다. 유사 feature를 추측하지 않는다.
- 원격 확인과 원문 조회가 모두 실패하면 non-zero exit로 종료한다.

## 실패 처리

- 원격 접속 실패, 권한 실패, DNS 실패, GitHub API 실패, git fallback 실패는 모두 최신성 확인 실패로 본다.
- 최신성 확인 실패 상태에서는 "캐시 기준으로 추정"하지 않는다.
- BE PRD 산출물이 없으면 PRD가 아직 생성되지 않은 상태로 보고한다.
- feature PRD가 없으면 사용 가능한 feature 후보를 보고하고 중단한다.
- 사용자에게 실패 원인과 stale 위험을 명시한다.

## 산출물 규칙

- `.cache/prd-read/`는 disposable cache이며 git에 커밋하지 않는다.
- FE projection 문서인 `docs/prd.md`, `docs/features/{feature}/prd.md`, `docs/traceability.md`는 후속 `$create-trd`, `$create-issues-adr` 입력을 위한 복사본이다. 이 문서의 내용 변경은 `$prd-read` 재실행 또는 BE PRD 갱신으로만 발생해야 한다.
- 캐시 metadata는 마지막으로 확인한 BE commit, 문서 목록 digest, 동기화 시각을 기록한다.
- `manifest.json`은 hub PRD, feature PRD 목록, traceability 문서 위치, 각 파일 sha256을 기록한다.
- `projection.json`은 마지막으로 projection한 FE-local 문서 경로와 BE commit/hash를 기록한다.
- 답변에는 가능하면 확인한 BE commit 또는 manifest sha256을 함께 적는다.
