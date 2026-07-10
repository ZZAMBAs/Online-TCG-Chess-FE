# Fragment Authoring Rules

## 기본 구조

```html
<section class="page-fragment page-fragment--<page-id>">
  <div class="layout-pair">
    <article class="viewport viewport--desktop actual-ui" aria-label="PC layout">
      <!-- 실제 PC 사용자 화면 의미 구조 -->
      <section class="interaction-state" aria-label="PC interaction result">
        <!-- PC에서 사용자 행동 이후 보이는 결과 -->
      </section>
    </article>
    <article class="viewport viewport--mobile actual-ui" aria-label="Mobile layout">
      <!-- 실제 모바일 사용자 화면 의미 구조 -->
      <section class="interaction-state" aria-label="Mobile interaction result">
        <!-- 모바일에서 사용자 행동 이후 보이는 결과 -->
      </section>
    </article>
  </div>

  <aside class="story-note">
    <!-- 화면 의미, 상호작용 의도, 구현 참고사항 -->
  </aside>

  <aside class="dev-state">
    <!-- FE 상태명, 서버 이벤트, 조건부 렌더링 키 -->
  </aside>
</section>
```

## 사용자 화면과 주석 분리

- `.actual-ui` 안에는 실제 제품 UI의 의미 구조만 둔다.
- `.story-note`에는 페이지 고유의 화면 의미, 상호작용 의도, 구현 참고사항만 둔다.
- `.dev-state`에는 사용자 문구처럼 보이면 안 되는 상태명, 이벤트명, 조건명을 둔다.
- "스토리보드 주석이란" 같은 공통 안내는 쓰지 않는다.
- `.actual-ui`에는 화면 목적을 판단할 수 있는 semantic form, input, button, list/table, board, dialog/sheet 구조를 둔다. 화면 전체를 설명 카드나 placeholder 문장만으로 대체하지 않는다.

## PC/Mobile

- PC와 Mobile은 같은 반응형 화면을 단순 축소하지 말고 별도 검토 영역으로 둔다.
- 모바일에서 먼저 보여줄 정보, CTA 위치, 모달/시트 표현이 다르면 구체적으로 다르게 그린다.
- 각 viewport 안에서 정보 우선순위, 주요 행동, 행동 이후 상태, 오류/권한 상태를 따로 표현한다.
- 고정 형식 UI는 구조가 이해되는 정도의 간단한 grid나 placeholder로 표현한다.

## 행동 이후 상태

- 사용자가 할 수 있는 주요 행동마다 결과 상태를 같은 fragment 안에 둔다.
- 예: 제출 성공, 검증 실패, 서버 거부, 모달 표시, 바텀시트, 대기 상태, 비활성 상태, 자동 이동.
- PC와 Mobile의 결과 표현이 다르면 각각의 `.interaction-state`에 따로 둔다.
- 행동 결과가 다른 페이지 이동이면 destination page id를 `.story-note`와 manifest `next`에 기록한다.
- 이후 목적지 fragment가 완성되면 예상 화면 표현을 동기화한다.

## CSS

- CSS는 렌더링 보조용 최소값만 사용한다.
- 허용 범위는 화면 영역 구분, PC/Mobile 비교 레이아웃, 상태/주석 영역 구분, 기본 가독성이다.
- 색상 팔레트, spacing, radius, typography, 실제 컴포넌트 스타일을 확정하지 않는다.
- Tailwind, styled-components, theme token, 컴포넌트 라이브러리 규칙을 흉내 내지 않는다.
- 페이지별 스타일을 추가하기보다 의미 있는 HTML 구조와 class 이름을 우선한다.
- `structure` fidelity에서는 실제 디자인을 흉내 내기 위한 색상·그림자·상세 spacing을 넣지 않는다.
- `visual_reference`가 있어도 해당 문서의 페이지 전용 CSS를 복사하지 않는다. 보존할 대상은 정보 위계, 영역 배치, CTA와 상태 표현이다.

## Manifest 갱신

- 변경한 page의 `status`를 실제 상태에 맞게 둔다: `draft`, `needs-review`, `approved`, `needs-revision`, `rejected`.
- `notes`에는 페이지 고유 변경점과 남은 질문을 적는다.
- `duplicate_check`에는 확인 대상과 결과를 남긴다.
- 하위 페이지 fragment를 작성하거나 수정하면 `parent_id`와 `entry_points`가 올바른지 확인한다.
- PC/Mobile 차이, 주요 상호작용 결과, TRD 이후 스타일링 결정 필요 항목을 `notes`나 `handoff`에 남긴다.
- 승인된 표현 원칙은 page note가 아니라 manifest의 `design_rules`에 둔다.
- 신규 page는 `fidelity: structure`로 시작한다. 참고 자산이 없으면 `visual_reference: null`을 유지하고 승인 차단 사유로 삼지 않는다.
- `representative_states`에는 fragment에서 실제로 비교 가능한 상태만 기록하고, `component_patterns`에는 구현 기술과 무관한 의미 패턴을 기록한다.
