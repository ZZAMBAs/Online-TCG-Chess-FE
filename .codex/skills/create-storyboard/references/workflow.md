# Storyboard Workflow

## 상태 파일

- `docs/design/storyboard-manifest.json`을 컨텍스트 압축 이후에도 다시 읽는 단일 상태 저장소로 사용한다.
- `docs/design/storyboard-pages.md`는 사람이 검토하는 페이지 분리안이다.
- 대화에서 확정된 표현 원칙, 승인/반려 이력, 중복 확인 결과, 다음 작업 후보를 manifest에 기록한다.
- 시각 디자인 세부값은 TRD 이후 확정 대상으로 남기고, manifest에는 화면 의미와 구현 참고사항을 우선 기록한다.

## Manifest 권장 구조

```json
{
  "version": 1,
  "spec": {
    "be_commit": "",
    "sha256": "",
    "checked_at": ""
  },
  "design_rules": [],
  "flow_summary": [],
  "handoff": [],
  "pages": [
    {
      "id": "lobby",
      "title": "로비",
      "parent_id": null,
      "status": "draft",
      "requirements": [],
      "fragment": "storyboard/fragments/lobby.html",
      "entry_points": [],
      "duplicate_check": {
        "checked_at": "",
        "matches": []
      },
      "fidelity": "structure",
      "visual_reference": null,
      "representative_states": [],
      "component_patterns": [],
      "notes": [],
      "next": []
    }
  ]
}
```

## 전체 흐름

1. `$spec-read` 성공 출력의 BE commit 또는 문서 sha256을 manifest에 기록한다.
2. `storyboard-manifest.json`과 `storyboard-pages.md`가 모두 있으면 기존 상태를 복원한다.
3. 상태 파일이 없으면 신규 프로젝트 bootstrap으로 보고 `$split-storyboard-pages`로 두 파일과 기본 page 목록을 만든다. 기존 fragment, tmp HTML, 통합 HTML이 없어도 정상 상태다.
4. 기존 storyboard 또는 참고 화면이 있으면 page별 `visual_reference` 후보로만 기록한다. 참고 자산이 없으면 `null`을 유지한다.
5. 페이지 분리안이 없거나 요구사항 변경으로 오래되었으면 `$split-storyboard-pages`로 갱신한다.
6. 만들거나 수정할 page id를 하나 고른다.
7. 새 페이지라면 존재하는 manifest, fragment, 참고 자산을 검색해 중복 여부를 기록한다.
8. `$create-storyboard-page <page-id>`로 해당 fragment만 작성하거나 수정한다.
9. 사용자가 승인하면 해당 page의 `status`를 `approved`로 바꾼다. 반려면 `needs-revision`과 반려 이유를 남긴다.
10. 통합이 필요하면 `scripts/build_storyboard.py`를 실행한다.
11. `rg "<iframe|srcdoc" docs/design/storyboard.html docs/design/storyboard/fragments`로 금지 요소를 확인한다.
12. manifest의 모든 page id가 `docs/design/storyboard.html`에 포함되는지 확인한다.
13. 브라우저 캡처로 확인했다면 검증 결과만 요약하고 캡처 파일은 삭제한다.

## Fidelity와 선택적 참고 자산

- `structure`: 기본값. 레이아웃 의미, 실제 입력/버튼/목록/보드 구조, 핵심 상태를 저스타일 HTML로 표현한다.
- `reference`: 승인된 기존 화면이나 시각 참고 자산을 연결한다. fragment는 참고 자산의 핵심 정보 구조만 보존한다.
- `prototype`: 별도 승인된 디자인 기준으로 대표 화면을 구체화한 경우에만 사용한다.
- `visual_reference`는 선택적 경로다. 없다는 이유로 페이지 작성이나 승인을 차단하지 않는다.
- 기존 manifest에 fidelity 필드가 없으면 `structure`, visual reference가 없으면 `null`로 해석해 호환한다.
- `representative_states`에는 화면 검토 가치가 큰 기본·오류·권한·실시간 상태만 기록한다.
- `component_patterns`는 후속 architecture/TRD에서 컴포넌트 경계를 추적하기 위한 의미 이름이며 구현 기술명을 넣지 않는다.

## 페이지 계층과 진입 경로

- 루트 페이지는 `parent_id: null`로 둔다.
- 하위 페이지는 정보 구조상 부모 page id를 `parent_id`에 하나만 기록한다.
- 여러 진입 경로는 `entry_points` 배열로 기록한다.
- 현재 페이지에서 이어지는 목적지는 `next` 배열로 기록한다.
- `parent_id`는 소유/계층을 의미하고, `entry_points`는 사용자가 도달할 수 있는 출발 화면을 의미한다.
- 예: `account-info`의 `parent_id`는 `my-page`이고, `entry_points`는 `["my-page", "settings"]`일 수 있다.

## 질문과 승인

- 질문은 한 번에 하나만 한다.
- 요구사항에서 알 수 있는 내용은 묻지 않는다.
- 요구사항 흐름, 화면 의미, 상호작용, PC/Mobile 우선순위를 바꾸는 선택지만 묻고, 추천안을 먼저 제시한다.
- 가벼운 문구나 구조 정리는 추가 질문 없이 반영할 수 있다.
- 색상, 간격, radius, typography 같은 실제 디자인 시스템 결정은 TRD 이후 항목으로 남긴다.
- 요구사항과 사용자 요청이 충돌하면 BE 요구사항을 우선하고 충돌 지점을 설명한다.

## 통합 규칙

- 최종 HTML은 렌더링 보조 CSS와 fragment를 한 문서로 조립한다.
- 상단에는 읽는 법, 화면 흐름 요약, 구현 핸드오프를 한 번만 둔다.
- 페이지별 fragment에는 공통 안내를 반복하지 않는다.
- tmp 독립 HTML은 최종 기준이 아니다. 필요한 경우 검토용으로만 만들고 manifest에 기준 산출물이 아님을 남긴다.

## 검증 캡처 정리

- 데스크톱/모바일 캡처는 검증 중 임시 파일로만 사용한다.
- 캡처 파일은 검증 결과를 확인하고 요약한 뒤 삭제한다.
- 캡처 파일을 git 추적 산출물이나 장기 보관 자료로 남기지 않는다.
- 실패 캡처도 사용자가 보관을 명시적으로 요청하지 않으면 삭제하고, 실패 내용은 텍스트로 요약한다.

## 저충실도 기준

- CSS는 화면 영역 구분, PC/Mobile 비교, 상태/주석 영역 구분, 기본 가독성에만 사용한다.
- Tailwind, styled-components, theme token, 컴포넌트 라이브러리 규칙을 흉내 내지 않는다.
- 실제 FE 스타일링 기술, 디자인 토큰, 상세 시각값은 TRD 이후 확정 대상으로 `handoff`나 page `notes`에 남긴다.
- 스토리보드의 핵심 정보는 화면 의미, 사용자 행동, 행동 이후 결과, 오류/권한 상태, 서버 이벤트, FE 조건부 렌더링 참고사항이다.
- 실제 폼, 목록, 표, 보드, 카드, dialog/sheet, CTA가 필요한 화면은 대응되는 semantic HTML 구조를 둔다. 이름만 적은 placeholder 카드로 화면 전체를 대체하지 않는다.
- 같은 페이지의 모든 상태를 고충실도로 복제하지 않고 기본 화면과 `representative_states`의 핵심 차이만 표현한다.
