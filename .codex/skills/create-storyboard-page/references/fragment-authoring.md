# Fragment Authoring Rules

## 공통 구조

```html
<section class="page-fragment page-fragment--<page-id>">
  <div class="layout-pair">
    <article class="viewport viewport--desktop actual-ui" aria-label="PC 화면">
      <!-- 실제 사용자 화면 -->
    </article>
    <article class="viewport viewport--mobile actual-ui" aria-label="Mobile 화면">
      <!-- 실제 사용자 화면 -->
    </article>
  </div>
  <section class="state-gallery" aria-label="대표 상호작용 상태">
    <!-- 기본 화면 전체를 복제하지 않고 달라지는 영역 중심 -->
  </section>
  <aside class="story-note"><!-- 화면 의미와 구현 참고 --></aside>
  <aside class="dev-state"><!-- FE/서버 상태명 --></aside>
</section>
```

## Structure 모드

- 사용자에게 필요한 실제 semantic element를 사용한다.
- 폼은 `form`, `label`, `input`, `button`으로, 목록/표/보드/dialog/sheet도 의미에 맞는 구조로 표현한다.
- 사용자 화면 전체를 설명 카드나 placeholder 문장으로 대체하지 않는다.
- 주요 행동의 성공, 검증 실패, 서버 거부, 대기, 권한, 자동 이동을 대표 상태로 둔다.
- PC와 Mobile의 정보 순서와 행동 위치를 별도로 작성한다.
- visual reference에서는 정보 위계와 상태만 가져온다.

## Visual 모드

- `design-baseline.md`의 draft 값을 읽고 공유 class로만 표현한다.
- class는 의미 패턴을 나타낸다. 예: `app-shell`, `ui-button`, `ui-card`, `ui-dialog`, `game-board`, `tcg-card`.
- 화면 밀도, 강조 순서, 상태 색, focus와 touch target을 baseline과 맞춘다.
- 페이지 고유 배치가 필요하면 semantic wrapper class를 fragment에 둘 수 있지만 CSS selector는 추가하지 않는다. 공유 가능한 surface인지 먼저 판단한다.
- 실제와 가까운 화면이어도 framework component명이나 production state명을 사용자 UI에 노출하지 않는다.

## 사용자 UI와 주석

- `.actual-ui`에는 실제 사용자가 보는 문구와 control만 둔다.
- `.story-note`에는 화면 고유 의도와 다음 page id를 둔다.
- `.dev-state`에는 이벤트명, 상태 조건, 동기화 기준을 둔다.
- 공통 읽는 법은 fragment마다 반복하지 않는다.

## 대표 상태

- 기본 상태는 desktop/mobile viewport에 표현한다.
- 대표 상태는 `state-gallery`에서 변경되는 panel, dialog, sheet, status만 보여준다.
- 오류 코드 목록 전체나 모든 가능한 조합을 시각화하지 않는다.
- 다른 page 이동이면 manifest `next`에 목적지를 기록한다.

## CSS 금지와 허용

- fragment의 `<style>`, `style` 속성, `iframe`, `srcdoc`을 금지한다.
- 페이지별 stylesheet와 `.page-fragment--<id> ...` selector를 금지한다.
- 공유 primitive 또는 product surface가 부족하면 `$create-storyboard` 디자인 패스에서 공통 CSS를 보강한다.
- CSS custom property 값은 `tokens.css`에서만 정의한다.

## Manifest 갱신

- structure 변경: `review.structure = needs-review`, `review.visual = blocked`.
- visual 변경: structure는 유지하고 `review.visual = needs-review`.
- 사용자 승인만 `approved`로 기록한다.
- `fidelity`는 structure 모드에서 `structure`, 시각화 후 `prototype`으로 둔다.
- `representative_states`에는 실제 fragment에 보이는 상태만 기록한다.
- `component_patterns`에는 구현 기술과 무관한 공유 UI 의미 이름을 기록한다.
- `visual_reference`와 재사용/제외 근거를 notes에 남긴다.
