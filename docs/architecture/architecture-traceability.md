# Architecture Traceability

| 결정 | 아키텍처 ADR | 출처 산출물 | 출처 섹션 | 반영 문서 | 상태 |
| --- | --- | --- | --- | --- | --- |
| React TypeScript Vite SPA | ARCH-ADR-001 | BE spec, reconfirmation | React client 전제, runtime 질문 | fixed-20260723/impl-fixed.md | accepted |
| 강화 TypeScript strict | ARCH-ADR-002 | interview | TypeScript 정책 | fixed-20260723/impl-fixed.md | accepted |
| 계층형 route config | ARCH-ADR-003 | storyboard, interview | page flow, routing 질문 | fixed-20260723/impl-fixed.md | accepted |
| 상태 소유권 분리 | ARCH-ADR-004 | BE spec, contracts | server authority, snapshot/replay replacement | fixed-20260723/impl-fixed.md | accepted |
| fetch/OpenAPI adapter | ARCH-ADR-005 | fixed REST contracts | REST/session/CSRF/closed schema | fixed-20260723/impl-fixed.md | accepted |
| STOMP manager와 resync | ARCH-ADR-006 | fixed STOMP contracts | STOMP snapshot/version/privacy | fixed-20260723/impl-fixed.md | accepted |
| module/import boundary | ARCH-ADR-007 | PRD map, interview | module 질문 | fixed-20260723/impl-fixed.md | accepted |
| CSS Modules와 token | ARCH-ADR-008 | design baseline, interview | semantic token, styling 질문 | fixed-20260723/impl-fixed.md | accepted |
| foundation Storybook | ARCH-ADR-009 | design baseline, interview | component pattern 질문 | fixed-20260723/impl-fixed.md | accepted |
| static same-site deployment | ARCH-ADR-010 | BE spec, interview | same-site session, deployment 질문 | fixed-20260723/infra-fixed.md | accepted |
| runtime public config | ARCH-ADR-011 | interview | environment 질문 | fixed-20260723/infra-fixed.md | accepted |
| npm/lockfile/engine | ARCH-ADR-012 | package.json, interview | package manager 질문 | fixed-20260723/harness-fixed.md | accepted |
| static analysis gates | ARCH-ADR-013 | architecture decisions, interview | harness 질문 | fixed-20260723/harness-fixed.md | accepted |
| shared MJS hook harness | ARCH-ADR-014 | interview | Git hook 질문 | fixed-20260723/harness-fixed.md | accepted |
| test layer responsibility | ARCH-ADR-015 | storyboard, interview | test 질문 | fixed-20260723/harness-fixed.md | accepted |
| contract drift gate | ARCH-ADR-016 | fixed contract projection | schema/fixture/manifest fingerprint | fixed-20260723/harness-fixed.md | accepted |
| dependency supply chain | ARCH-ADR-017 | package policy, interview | supply-chain 질문 | fixed-20260723/harness-fixed.md | accepted |
| immutable artifact promotion | ARCH-ADR-018 | infra decisions, interview | CI/CD 질문 | fixed-20260723/harness-fixed.md | accepted |
| JSON Schema Ajv validation | ARCH-ADR-019 | fixed schema contracts | pre-reducer closed schema validation | fixed-20260723/harness-fixed.md | accepted |
