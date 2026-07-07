---
name: create-storyboard-page
description: Online-TCG-Chess-FE 저충실도 스토리보드에서 특정 page id의 docs/design/storyboard/fragments/*.html fragment를 생성하거나 수정한다. PC/Mobile 의미 구조, 각 화면의 상호작용 결과, 오류/권한 상태, story-note/dev-state 구현 참고사항, manifest 상태 갱신이 필요한 페이지 단위 작업에 사용한다.
---

# Create Storyboard Page

## 역할

- 하나의 page id에 해당하는 body fragment를 생성하거나 수정한다.
- 실제 사용자 UI와 구현 주석을 분리한다.
- PC 화면, 모바일 화면, 각 화면의 행동 이후 상태를 같은 fragment 안에서 검토 가능하게 표현한다.
- CSS 세부 구현보다 화면 의미, 사용자 행동, 상태 변화, 구현 참고사항을 우선한다.
- 최종 통합은 하지 않는다. 통합은 `$create-storyboard`의 빌드 스크립트가 담당한다.

## 절차

1. `$spec-read`로 BE 요구사항 최신성을 확인한다. 이미 같은 턴에서 성공했다면 확인된 commit 또는 sha256을 사용한다.
2. 작업 전에 `references/fragment-authoring.md`를 읽는다.
3. `docs/design/storyboard-manifest.json`에서 대상 page id를 찾는다.
4. 대상 fragment만 읽는다. 전체 `docs/design/storyboard.html`을 먼저 읽지 않는다.
5. 새 fragment라면 manifest와 기존 fragments에서 중복 여부를 다시 확인한다.
6. 화면을 작성하거나 수정한 뒤 manifest의 해당 page에 상태, 승인 필요 여부, 변경 notes를 남긴다.

## Fragment 위치

- 기본 경로는 `docs/design/storyboard/fragments/<page-id>.html`이다.
- manifest의 `pages[].fragment`가 있으면 그 경로를 따른다.
- fragment는 `<body>` 전체 문서가 아니라 통합본에 삽입될 body 조각이다.

## 작성 원칙

- 실제 사용자가 보는 UI는 `.actual-ui` 영역에 둔다.
- 실제 UI에는 사용자에게 노출되는 문구, 버튼, 카드, 모달, 인라인 피드백, 오버레이만 넣는다.
- 요구사항 설명, 구현 의도, BE/FE 조건, 개발 상태명은 `.story-note` 또는 `.dev-state`로 화면 밖에 둔다.
- 공통 읽는 법이나 반복 안내 카드는 fragment에 넣지 않는다.
- CSS는 가독성 보조 수준으로만 사용하고, 실제 FE 디자인 시스템이나 스타일링 기술을 확정하지 않는다.
- `iframe`과 `srcdoc`은 사용하지 않는다.
- 앱 소스코드와 BE 요구사항 문서는 수정하지 않는다.
