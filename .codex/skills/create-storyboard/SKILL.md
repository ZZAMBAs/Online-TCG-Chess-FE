---
name: create-storyboard
description: Online-TCG-Chess-FE에서 BE 요구사항 기반 화면 구조부터 공통 디자인 기준을 적용한 실제에 가까운 PC/Mobile 정적 화면까지 하나의 승인형 workflow로 생성·갱신한다. 페이지 분리, 구조 승인, $design-decision draft, 공통 token/primitive CSS, 시각 승인, manifest 상태 관리와 docs/design/storyboard.html 통합이 필요할 때 사용한다.
---

# Create Storyboard

## 역할

- 사용자에게 노출되는 단일 스토리보드 진입점으로 동작한다.
- 내부 작업을 `구조 작성 → 구조 승인 → 디자인 초안 → 시각 렌더링 → 시각 승인`으로 분리한다.
- 페이지 분리는 `$split-storyboard-pages`, 페이지 작성은 `$create-storyboard-page`, 공통 디자인 기준은 `$design-decision`에 위임한다.
- 최종 산출물은 실제 구현 결과를 예측할 수 있는 정적 `docs/design/storyboard.html`이다.
- 앱 소스 구현과 프레임워크별 CSS 구조는 후속 architecture/TDD가 담당한다.

## 시작 절차

1. `$spec-read`와 `$prd-read`로 BE `master` 최신성을 확인한다. 하나라도 실패하면 중단한다.
2. `references/workflow.md`를 읽는다.
3. manifest와 페이지 분리안이 없으면 `$split-storyboard-pages`로 bootstrap한다.
4. 기존 manifest, fragments, storyboard와 명시적으로 제공된 외부 참고 자산에서 중복과 시각 참고 후보를 확인한다.
5. manifest의 `workflow_stage`와 페이지별 `review.structure`, `review.visual`을 기준으로 다음 단계 하나만 수행한다.

## 승인 단계

- `structure-draft`: 페이지 구조와 대표 상태를 작성한다.
- `structure-review`: 사용자에게 화면 목적, 흐름, PC/Mobile 우선순위 승인을 요청한다.
- `design-draft`: 모든 구조가 승인되면 `$design-decision`으로 draft baseline과 공통 CSS 계약을 만든다.
- `visual-review`: draft baseline을 공통 CSS로 모든 fragment에 적용하고 실제에 가까운 화면 승인을 요청한다.
- `approved`: 모든 시각 승인과 baseline 승인이 끝난 상태다.

구조가 바뀐 페이지는 `review.visual`을 `blocked`로 되돌리고 디자인 영향을 재검토한다.

## 산출물

- `docs/design/storyboard-manifest.json`: workflow stage, source hash, 페이지 구조/시각 승인, 참고 자산, 대표 상태
- `docs/design/storyboard-pages.md`: 사람이 검토하는 페이지 분리안
- `docs/design/design-baseline.md`: draft 또는 approved 디자인 기준
- `docs/design/storyboard/fragments/*.html`: 페이지별 PC/Mobile 사용자 화면과 대표 상태
- `docs/design/storyboard/styles/tokens.css`: semantic token
- `docs/design/storyboard/styles/primitives.css`: 공통 UI primitive
- `docs/design/storyboard/styles/product-surfaces.css`: 체스·TCG 카드·채팅·관리자 표 같은 제품 고유 표면
- `docs/design/storyboard.html`: 통합 검토본

## 시각화 원칙

- 구조 단계에서는 실제 폼, 목록, 보드, CTA와 상태를 저스타일로 표현한다.
- 시각 단계에서는 draft baseline의 token과 공유 class만 사용해 사용자 화면에 가까운 밀도와 위계를 표현한다.
- 기본 화면과 검토 가치가 큰 대표 상태만 전체 화면으로 보여주고, 나머지 상태는 차이 영역만 표현한다.
- PC와 Mobile은 축소 관계가 아니라 별도 정보 우선순위와 행동 배치를 가진다.
- 페이지별 CSS, fragment 내부 `<style>`, `style` 속성, page id 전용 selector를 만들지 않는다.

## 통합과 검증

```bash
python3 .codex/skills/create-storyboard/scripts/build_storyboard.py
```

- `iframe`, `srcdoc`, fragment의 `<style>`과 `style` 속성을 금지한다.
- manifest의 모든 page id가 통합본에 포함되는지 확인한다.
- desktop/mobile을 정적 파일로 시각 검증한다.
- 검증 캡처는 요약 후 삭제한다.
- 사용자 승인 없이 구조·시각 상태나 baseline을 `approved`로 표시하지 않는다.

## 후속 단계

- 최종 승인 후 `$architecture-decision`으로 CSS 기술, production token 위치, component boundary와 visual gate를 확정한다.
- storyboard HTML을 앱 코드로 그대로 복사하도록 강제하지 않는다. 승인된 token, variant, 정보 구조와 상태 표현을 구현 계약으로 넘긴다.

## 금지 사항

- 앱 소스, 앱 설정, BE 원문, architecture, TRD를 수정하지 않는다.
- 구조 승인 전에 고충실도 페이지 전체를 작성하지 않는다.
- draft 디자인 값을 production 확정값으로 취급하지 않는다.
- 모든 상태를 전체 화면으로 복제하거나 페이지마다 CSS를 작성하지 않는다.
