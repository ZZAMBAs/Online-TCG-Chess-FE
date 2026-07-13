# Storyboard Workflow

## 상태 저장소

`docs/design/storyboard-manifest.json`을 단일 실행 상태 저장소로 사용한다. 대화 내용보다 manifest를 우선한다.

```json
{
  "version": 2,
  "workflow_stage": "structure-review",
  "design": {
    "baseline": "design-baseline.md",
    "baseline_status": "blocked"
  },
  "pages": [
    {
      "id": "lobby-quick-match",
      "review": {
        "structure": "needs-review",
        "visual": "blocked"
      },
      "fidelity": "structure",
      "visual_reference": null
    }
  ]
}
```

허용 page review 상태는 `draft`, `needs-review`, `approved`, `needs-revision`, `rejected`, `blocked`다.

## 상태 전이

1. `structure-draft`
   - `$split-storyboard-pages`로 page map을 만든다.
   - `$create-storyboard-page` structure 모드로 fragment를 작성한다.
   - 신규/수정 page는 structure `needs-review`, visual `blocked`다.
2. `structure-review`
   - 화면 목적, 흐름, PC/Mobile 우선순위, 대표 상태를 사용자에게 검토받는다.
   - 모든 structure가 approved일 때만 다음 단계로 간다.
3. `design-draft`
   - `$design-decision`으로 draft baseline과 공유 CSS 계약을 만든다.
   - tmp나 외부 참고 화면은 시각 방향 후보로만 사용한다.
4. `visual-review`
   - `$create-storyboard-page` visual 모드로 모든 페이지에 같은 디자인 문법을 적용한다.
   - 기본 화면과 대표 상태를 desktop/mobile에서 검토한다.
5. `approved`
   - 모든 visual review와 baseline을 사용자 승인 후 함께 approved로 확정한다.
   - `$architecture-decision`으로 넘긴다.

구조가 바뀌면 해당 page의 visual을 blocked로 바꾸고, 이미 approved인 baseline은 `needs-review`로 되돌린다.

## 기존 상태 호환

- version 1의 `page.status`는 구조 상태로 읽는다.
- migration 시 `review.structure = status`, `review.visual = blocked`로 옮긴다.
- 기존 `status`는 새 승인 판단에 사용하지 않는다.
- 기존 fidelity가 없으면 `structure`, visual reference가 없으면 `null`로 해석한다.

## 선택적 참고 자산

- 사용자가 명시적으로 제공한 외부 참고 자산만 `visual_reference`로 기록한다.
- 참고 자산이 없으면 `null`을 유지하고 요구사항, PRD, 승인된 구조와 디자인 결정만으로 작성한다.
- 참고 자산의 독립 CSS를 복사하지 않고 정보 위계와 상태 표현만 참고한다.
- 참고 자산 부재를 구조 또는 시각 작성의 차단 사유로 삼지 않는다.

## 공유 CSS 경계

- `tokens.css`: 의미 기반 값만 둔다.
- `primitives.css`: app shell, navigation, button, input, card, list, table, dialog/sheet, status를 둔다.
- `product-surfaces.css`: board, game HUD, TCG card, hand, chat, admin workspace를 둔다.
- fragment 내부 `<style>`, `style` 속성, page id selector, 페이지별 stylesheet를 금지한다.
- CSS 기술과 production 파일 위치는 architecture가 결정한다.

## 질문과 승인

- 구조 단계에서는 흐름·화면 의미·반응형 우선순위만 묻는다.
- 디자인 단계에서는 전역 시각 방향·density·접근성에 영향을 주는 선택만 묻는다.
- 질문은 한 번에 하나만 하고 추천안을 먼저 제시한다.
- 사용자 승인 없이 상태를 approved로 바꾸지 않는다.
- 구조 승인과 시각 승인을 하나의 표현으로 합치지 않는다.

## 통합 검증

1. build script로 통합한다.
2. 금지 요소와 누락 page id를 검사한다.
3. manifest stage와 page review 조합이 유효한지 검사한다.
4. desktop/mobile에서 가로 넘침, 겹침, 읽기 순서와 대표 상태를 확인한다.
5. 캡처 결과를 요약하고 파일은 삭제한다.

## 구현 handoff

- 승인된 token 이름/값, component variant, responsive/a11y 규칙을 넘긴다.
- storyboard HTML 자체를 production component 계약으로 간주하지 않는다.
- 라우팅, 상태 소유권, CSS 기술과 실제 component boundary는 architecture/TRD에서 확정한다.
