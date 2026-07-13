---
name: create-storyboard-page
description: Online-TCG-Chess-FE storyboard의 특정 page id를 structure 또는 visual 모드로 생성·수정한다. PC/Mobile 의미 구조, 실제 폼·목록·보드, 상호작용 결과, 오류·권한 상태를 작성하거나 승인된 구조에 draft 디자인 baseline과 공통 CSS class를 적용할 때 사용한다.
---

# Create Storyboard Page

## 역할

- 하나의 page id에 해당하는 body fragment만 작성한다.
- `structure` 모드와 `visual` 모드를 명확히 구분한다.
- 최종 통합과 공통 CSS 작성은 `$create-storyboard`가 담당한다.

## 절차

1. 같은 workflow turn에서 확인한 `$spec-read`와 `$prd-read` commit/hash를 사용한다. 없으면 먼저 확인한다.
2. `references/fragment-authoring.md`를 읽는다.
3. manifest에서 page id, workflow stage, review 상태, visual reference를 확인한다.
4. 대상 fragment와 해당 visual reference만 읽는다. 통합 HTML 전체를 먼저 읽지 않는다.
5. 요청 모드의 gate를 확인하고 fragment를 작성한다.
6. 대표 상태와 component pattern, 변경 note, 해당 review 상태를 manifest에 기록한다.

## Structure 모드

- `structure-draft` 또는 구조 재검토에서 사용한다.
- 실제 사용자 목적을 판단할 수 있는 semantic form, list, table, board, dialog/sheet, CTA를 작성한다.
- PC/Mobile 정보 우선순위와 행동 이후 결과를 분리한다.
- visual reference가 있으면 정보 위계·상태·조작 의미를 재사용하되 CSS를 복사하지 않는다.
- 변경 후 `review.structure`을 `needs-review`, `review.visual`을 `blocked`로 둔다.

## Visual 모드

- `review.structure == approved`이고 `design-baseline.md`가 `draft` 또는 `needs-review`일 때만 사용한다.
- baseline에 정의된 token과 공유 primitive/product-surface class만 적용한다.
- 실제 사용자 화면에 가까운 밀도, 위계, 상태 표현을 만든다.
- fragment에 `<style>`, `style` 속성, 페이지 전용 CSS를 추가하지 않는다.
- 변경 후 `review.visual`을 `needs-review`로 둔다.

## Fragment 규칙

- 위치는 manifest의 `fragment` 또는 `docs/design/storyboard/fragments/<page-id>.html`이다.
- `.actual-ui`에는 사용자에게 보이는 UI만 둔다.
- `.story-note`와 `.dev-state`에는 화면 밖 구현·서버 상태 참고만 둔다.
- `iframe`과 `srcdoc`을 사용하지 않는다.
- 앱 소스와 요구사항 원문을 수정하지 않는다.
