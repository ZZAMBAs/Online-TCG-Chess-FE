# 에이전트 지침

이 저장소는 Online-TCG-Chess의 프론트엔드 파트다.

요구사항 확인, 기능 동작 판단, 구현 계획, REST/STOMP 계약 검토처럼 BE 요구사항
확인이 필요한 작업은 프로젝트 로컬 `$spec-read` 스킬을 사용한다.

FE 로컬 추정과 BE 요구사항이 충돌하면 BE 요구사항을 우선한다.

FE 계약 projection은 canonical BE repo의 전체 협상 session이 `completed`이고 모든 summary가 `fixed`인 경우에만 `$sync-fe-contracts`로 동기화한다. topic별 부분 sync는 하지 않는다.

이 `AGENTS.md`는 항상 150줄 이하로 유지하고, 상세 절차는 스킬에 둔다.
