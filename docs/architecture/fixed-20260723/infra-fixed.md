# FE Infrastructure Fixed

## Status and Sources

- status: fixed
- fixed_date: 20260723
- related ADR: `ARCH-ADR-010`, `ARCH-ADR-011`, `ARCH-ADR-018`

## Reconfirmed Infrastructure

- Vite static SPA artifact는 same-site HTTPS entry에서 제공하고, entry가 history fallback, REST proxy, WebSocket upgrade와 security header를 단일 소유한다.
- main artifact를 한 번 build해 stage/prod에 checksum 그대로 승격하며, 환경 차이는 runtime public config로 주입한다.
- API/WebSocket response는 CDN cache 대상이 아니며, content-hashed asset만 immutable cache를 사용한다.
- CSP report-only 후 enforce, private sourcemap upload, 비민감 observability adapter와 기존 secret/header 원칙을 유지한다.

## Contract Impact

- canonical contract bundle의 runtime location과 hosting/vendor/path는 아직 확정되지 않았다. 동일 origin과 contract schema 검증 원칙을 바꾸지 않는 범위에서만 운영 설정으로 결정한다.
