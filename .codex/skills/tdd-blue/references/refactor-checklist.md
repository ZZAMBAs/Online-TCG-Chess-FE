# Refactor Checklist

BLUE에서는 GREEN으로 통과한 동작을 유지한 채 production 코드만 정리한다. 아래 항목 중 실제 개선 가치가 있는 것만 적용하고, 리팩터링할 부분이 없으면 수정하지 않는다.

## 설계 점검

- 단일 책임: page, component, composable, store, API/STOMP client 함수가 하나의 명확한 이유로 변경되는지 확인한다.
- 의존 방향: 아키텍처 문서의 routing, state ownership, component, adapter 방향을 거스르지 않는다.
- 캡슐화: 불필요하게 public surface를 늘리지 않는다.
- 응집도: 함께 변하는 데이터와 동작이 지나치게 흩어져 있지 않은지 확인한다.
- 결합도: 테스트 통과를 위해 구체 구현에 과도하게 묶인 의존이 생기지 않았는지 확인한다.

## 코드 정리

- 중복: 같은 조건, 변환, 검증, 예외 처리가 반복되면 의미 있는 단위로 합친다.
- 네이밍: 도메인 의미와 책임이 드러나도록 component, composable, store action, API method, 변수명을 정리한다.
- 컨벤션: 기존 코드의 폴더, export, props/events, store, route, API client, 오류 처리 스타일과 맞춘다.
- 복잡도: 분기와 메서드 길이가 읽기 어렵다면 의미 단위로 나눈다.

## 오버엔지니어링 경계

- 현재 AC와 GREEN 테스트가 요구하지 않는 확장 포인트를 만들지 않는다.
- 전략, factory, 공통 composable, 공통 component, 공통 util은 중복이나 책임 분리를 실제로 줄일 때만 만든다.
- 한 번만 쓰이는 단순 로직을 억지로 추상화하지 않는다.
- 향후 기능을 예측해 public props/events, store surface, API client surface를 넓히지 않는다.
