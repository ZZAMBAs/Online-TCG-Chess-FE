---
name: spec-read
description: Online-TCG-Chess-FE에서 백엔드 요구사항을 확인, 분석, 구현 계획, 기능 동작 판단, REST/STOMP 계약 검토에 사용한다. BE 저장소 master의 docs/spec/spec-fixed.md를 원격 최신성 확인 후 읽고, 원격 확인 실패 시 캐시가 있어도 요구사항 기반 작업을 중단한다.
---

# Spec Read

## 원칙

- BE 요구사항 원문은 `ZZAMBAs/Online-TCG-Chess-BE`의 `master` 브랜치
  `docs/spec/spec-fixed.md`다.
- FE 저장소에 요구사항 원문을 권위 문서로 복사하지 않는다.
- 요구사항 기반 답변, 구현 계획, 코드 변경 전에는 원격 최신성을 먼저 확인한다.
- 원격 최신성 확인에 실패하면 캐시가 있어도 사용하지 않는다.
- 실패 시 stale 위험을 사용자에게 알리고 요구사항 기반 작업을 중단한다.

## 기본 절차

1. 저장소 루트에서 helper를 실행한다.

   ```bash
   python3 .codex/skills/spec-read/scripts/read_be_spec.py
   ```

2. helper가 성공하면 출력된 캐시 파일을 읽어 요구사항을 분석한다.
3. helper가 실패하면 캐시를 열지 말고 작업을 중단한다.
4. REST/STOMP처럼 외부 노출 계약을 다루면, 요구사항 확인 후 contract freeze 여부도 확인한다.

## Helper 동작

- 먼저 원격 `master` HEAD를 확인해 캐시가 최신인지 판단한다.
- 캐시가 최신이면 `.cache/spec-read/spec-fixed.md`를 재사용한다.
- 원격 HEAD가 바뀌었거나 캐시가 없으면 요구사항 원문을 다시 받는다.
- 원문 조회 순서는 raw GitHub URL, `gh api`, `.cache/spec-read/be-repo` shallow clone 재사용 순서다.
- 원격 확인과 원문 조회가 모두 실패하면 non-zero exit로 종료한다.

## 실패 처리

- 원격 접속 실패, 권한 실패, DNS 실패, GitHub API 실패, git fallback 실패는 모두 최신성 확인 실패로 본다.
- 최신성 확인 실패 상태에서는 "캐시 기준으로 추정"하지 않는다.
- 사용자에게 원격 확인 실패와 stale 위험을 명시한다.

## 산출물 규칙

- `.cache/spec-read/`는 disposable cache이며 git에 커밋하지 않는다.
- 캐시 metadata는 마지막으로 확인한 BE commit, 문서 sha256, 동기화 시각을 기록한다.
- 답변에는 가능하면 확인한 BE commit 또는 문서 sha256을 함께 적는다.
