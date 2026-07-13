---
name: create-storyboard
description: Online-TCG-Chess-FE에서 BE 요구사항을 $spec-read로 확인한 뒤 저충실도 스토리보드 워크플로우를 지휘한다. 페이지 분리($split-storyboard-pages), PC/Mobile 의미 구조와 상호작용 상태 fragment 생성/수정($create-storyboard-page), manifest 상태 관리, docs/design/storyboard.html 최종 통합과 검증이 필요한 작업에 사용한다.
---

# Create Storyboard

## 역할

- `$create-storyboard`는 스토리보드 워크플로우를 조율하는 상위 스킬이다.
- BE 요구사항 확인은 항상 `$spec-read`로 시작한다.
- 페이지 분리는 `$split-storyboard-pages`, 개별 화면 작성은 `$create-storyboard-page`를 사용한다.
- 최종 산출물은 `docs/design/storyboard.html`이며, 통합은 `scripts/build_storyboard.py`로만 수행한다.
- 스토리보드는 시각 디자인 확정물이 아니라 요구사항 흐름, 상태 변화, PC/Mobile 정보 우선순위, FE 구현 참고사항을 검증하는 저충실도 산출물이다.

## 시작 절차

1. `$spec-read`를 사용해 BE `master`의 `docs/spec/spec-fixed.md` 최신성을 확인한다.
2. 원격 최신성 확인이 실패하면 캐시를 열지 말고 스토리보드 작업을 중단한다.
3. 작업 전에 `references/workflow.md`를 읽고 상태 파일과 승인 규칙을 따른다.
4. `docs/design/storyboard-manifest.json`과 `docs/design/storyboard-pages.md`가 있으면 먼저 읽는다.
5. 두 상태 파일이 없으면 신규 프로젝트 bootstrap으로 보고 `$split-storyboard-pages`가 새 상태 파일을 만들도록 한다. 기존 storyboard, fragment, visual reference가 없어도 중단하지 않는다.
6. 새 페이지를 만들기 전에 존재하는 manifest, fragment, 기존 storyboard/참고 화면에서 중복 여부를 확인한다. 참고 화면 재사용은 선택 사항이며 필수 입력이 아니다.

## 산출물

- `docs/design/storyboard-manifest.json`: 페이지 목록, 요구사항 추적, 승인 상태, 중복 확인, 디자인 결정, 다음 작업 상태
- `docs/design/storyboard-pages.md`: 사람이 읽는 페이지 분리안
- `docs/design/storyboard/fragments/*.html`: 페이지별 의미 구조, PC/Mobile 화면, 상호작용 상태 body fragment
- `docs/design/storyboard/styles/*.css`: 렌더링 보조용 최소 CSS. 실제 FE 디자인 시스템이나 스타일링 기술을 확정하지 않는다.
- `docs/design/storyboard.html`: 빌드 결과물

## 표현 수준

- 기본 fidelity는 `structure`다. 실제 폼, 목록, 보드, 모달, CTA의 의미 구조와 주요 상태는 화면처럼 표현하되 상세 시각값은 확정하지 않는다.
- 기존 참고 화면이 있으면 `visual_reference`로 연결할 수 있지만 해당 HTML/CSS를 fragment에 복제하지 않는다.
- `reference`나 `prototype` fidelity는 기존 참고 자산 또는 별도 승인된 디자인 기준이 있을 때만 사용한다.
- 저충실도는 저스타일을 뜻한다. 화면 정보와 상호작용을 단순 텍스트 요약으로 축소하지 않는다.

## 통합

- 모든 통합은 아래 명령으로 수행한다.

```bash
python3 .codex/skills/create-storyboard/scripts/build_storyboard.py
```

- `iframe`과 `srcdoc`은 사용하지 않는다.
- 정적 HTML이므로 개발 서버를 띄우지 말고 브라우저에서 파일로 확인한다.
- 가능하면 headless Chrome 또는 Playwright로 데스크톱/모바일 캡처를 확인한다.
- 캡처 파일은 검증 결과를 요약한 뒤 삭제하고 산출물로 남기지 않는다.

## 금지 사항

- 앱 소스코드, 앱 설정, BE 요구사항 문서는 수정하지 않는다.
- BE 요구사항 원문을 FE 저장소에 권위 문서로 복사하지 않는다.
- 사용자 승인 없이 승인되지 않은 페이지를 최종 확정 상태로 표시하지 않는다.
- 대화 컨텍스트만 믿고 이어가지 말고 manifest를 상태 저장소로 사용한다.
- 관련 페이지가 승인되면 다음 단계로 `$design-decision`을 안내한다. 스토리보드에서 실제 design token이나 production CSS를 확정하지 않는다.
