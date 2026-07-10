---
name: split-storyboard-pages
description: Online-TCG-Chess-FE에서 BE 요구사항 확인 뒤 스토리보드 페이지 분리안을 만든다. docs/design/storyboard-pages.md와 docs/design/storyboard-manifest.json의 pages, 요구사항 추적, 중복 확인 상태를 생성하거나 갱신할 때 사용한다.
---

# Split Storyboard Pages

## 역할

- BE 요구사항에서 실제 사용자 화면 단위의 페이지 목록을 도출한다.
- 결과는 `docs/design/storyboard-pages.md`와 `docs/design/storyboard-manifest.json`에 기록한다.
- 이미 fragment가 있는 요구사항은 새 페이지로 중복 생성하지 않고 기존 page id에 연결한다.

## 절차

1. 먼저 `$spec-read`로 BE 요구사항 최신성을 확인한다. 실패하면 작업을 중단한다.
2. 작업 전에 `references/page-split.md`를 읽는다.
3. 기존 `storyboard-manifest.json`, `storyboard-pages.md`, `storyboard/fragments/*.html`이 있으면 확인한다. 모두 없으면 신규 bootstrap으로 진행한다.
4. 요구사항별 사용자 목표, 진입점, 행동 이후 상태, 오류/권한 상태를 묶어 페이지 후보를 만든다.
5. 기존 페이지와 중복되는 후보는 새 id를 만들지 말고 manifest의 해당 page에 요구사항과 note를 추가한다. 기존 산출물이 없으면 중복 없음으로 기록한다.
6. 확정 전 사용자가 판단해야 하는 디자인 질문은 한 번에 하나만 묻는다.
7. `storyboard-pages.md`와 manifest를 함께 갱신한다.

## 산출 기준

- page id는 lowercase kebab-case로 쓴다.
- 루트 페이지는 `parent_id: null`, 하위 페이지는 단일 부모 page id를 `parent_id`에 기록한다.
- 여러 진입 경로는 `entry_points` 배열로 기록한다.
- PC/Mobile이 정보 우선순위나 행동 배치가 다르면 같은 page id 안의 별도 상태로 기록한다.
- 행동 결과가 다른 페이지 이동이면 목적지 page id를 명시한다.
- 아직 목적지 fragment가 없으면 `next`에 후보로 남긴다.
- 신규 page에는 `fidelity: structure`, `visual_reference: null`, 빈 `representative_states`와 `component_patterns`를 기본값으로 기록한다.
- split 단계에서는 사용자 화면 HTML을 작성하지 않는다. HTML은 `$create-storyboard-page`가 담당한다.
