# MJS Harness Template

Git hook 또는 CI에서 재사용할 Node `.mjs` guard를 설계할 때 이 기준을 따른다.

## 결정할 항목

- 실행 위치: pre-commit, pre-push, CI required check 중 어디에서 실행할지 정한다.
- 입력 파일 수집: staged files, changed files, 전체 repo 중 어느 범위를 검사할지 정한다.
- lint-staged 연계: lint-staged가 넘긴 파일 인자를 받을지, 자체적으로 git diff를 읽을지 정한다.
- 검사 방식: 단순 문자열 검색, 정규식, AST/parser, JSON/YAML parser 중 어떤 방식을 쓸지 정한다.
- ignore 정책: generated, dist, coverage, snapshots, test artifacts, vendored files 제외 기준을 정한다.
- 출력 형식: 실패 파일, 규칙 id, 이유, 수정 힌트를 포함한다.
- exit code: 위반 없음은 0, 위반은 1, 도구 오류는 2처럼 구분한다.
- bypass 정책: 긴급 우회 허용 여부와 허용한다면 PR 설명/후속 issue 요구 여부를 정한다.
- Node version: package engine 또는 CI version과 맞춘다.
- CI 재사용: hook과 CI가 같은 엔트리포인트를 호출하게 한다.
- fixture 테스트: pass/fail fixture와 expected output을 둔다.

## 문서화 항목

- guard 이름과 목적
- 금지하거나 강제하는 패턴
- 입력 파일 범위
- parser와 dependency
- hook 연결 방식
- CI required check 여부
- 실패 메시지 예시
- fixture 테스트 위치
- 우회 조건과 승인자
