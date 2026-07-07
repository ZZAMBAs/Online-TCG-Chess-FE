# Page Split Rules

## 입력

- `$spec-read`가 확인한 BE 요구사항 캐시
- `docs/design/storyboard-manifest.json`
- `docs/design/storyboard-pages.md`
- `docs/design/storyboard/fragments/*.html`

## 페이지 분리 기준

- 사용자가 다른 목적을 달성하면 별도 페이지 후보로 분리한다.
- 같은 URL 또는 같은 화면이라도 행동 이후 상태가 크고 검토가 필요하면 같은 page id 안의 상태로 둔다.
- 모달, 바텀시트, 오류, 권한 거부, 서버 대기, 자동 이동은 원칙적으로 해당 행동을 시작한 page id에 포함한다.
- 목적지 화면을 사용자가 따로 검토해야 하면 별도 page id로 분리한다.
- 관리자/플레이어/관전자처럼 권한별 정보 우선순위가 다르면 같은 page id의 variant 또는 별도 page id 중 더 구현에 가까운 형태를 선택한다.
- 하위 페이지라도 독립 사용자 목적이 있으면 별도 page id로 분리하고 `parent_id`로 부모를 연결한다.
- 부모-자식 관계와 진입 경로를 섞지 않는다. 부모는 `parent_id` 하나, 진입 경로는 `entry_points` 배열로 관리한다.

## 중복 확인

- 새 page id를 만들기 전에 manifest의 `pages[].requirements`, `pages[].notes`, `pages[].id`, `pages[].title`을 확인한다.
- `docs/design/storyboard/fragments/*.html`에서 요구사항 키워드, 화면명, 주요 버튼 문구를 검색한다.
- 중복이면 새 파일을 만들지 말고 기존 page에 다음 정보를 추가한다.
  - 연결된 요구사항
  - 보강해야 할 상태
  - 중복 확인 시각 또는 근거

## storyboard-pages.md 형식

```markdown
# Storyboard Pages

## 기준

- BE spec: <commit 또는 sha256>
- 디자인 규칙: <확정된 톤앤매너>

## Pages

### lobby

- 목적:
- 부모 page id:
- 진입 경로:
- 담당 요구사항:
- 주요 행동:
- 행동 이후 상태:
- PC/Mobile 차이:
- 오류/권한 상태:
- 중복 확인:
- 다음 작업:
```

## manifest 갱신

- `spec.be_commit` 또는 `spec.sha256`을 기록한다.
- `pages` 순서는 최종 HTML 탐색 순서로 둔다.
- 새 페이지의 초기 `status`는 `draft` 또는 `needs-review`로 둔다.
- 루트 페이지는 `parent_id: null`로 둔다.
- 하위 페이지는 `parent_id`에 단일 부모 page id를 둔다.
- 여러 화면에서 진입 가능하면 `entry_points`에 모든 출발 page id를 둔다.
- 사용자가 승인한 페이지만 `approved`로 둔다.
- 다음 턴에 이어갈 수 있도록 `next`나 `handoff`에 작업 후보를 남긴다.
