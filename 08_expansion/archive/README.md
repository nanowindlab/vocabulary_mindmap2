# 08_expansion Archive Guide

> Role: 프로젝트 문서 아카이브의 canonical zone

## Scope

이 폴더는 `08_expansion/`에서 파생된 문서형 산출물의 history 보관소다.

- `historical_docs/`
  - 구버전 spec, tasklist, protocol, 구조 문서
- `audit_logs/`
  - 특정 시점 검증 보고서, 리뷰 메모, 일시적 감사 산출물

## Rule

- 현재 SSOT 문서를 이 폴더에서 직접 읽지 않는다.
- 최신 canonical 문서는 항상 `08_expansion/` 루트의 현재 버전을 먼저 본다.
- 구버전 비교, 의사결정 이력 추적, audit evidence 확인이 필요할 때만 사용한다.

## Canonical History Policy

문서형 history의 canonical 보관 위치는 현재 이 폴더다.

- 구버전 spec
- 구버전 tasklist
- 구버전 protocol
- 구조 변경 감사 문서
- review memo 및 audit report

top-level `archive/`는 문서형 SSOT archive가 아니라 legacy session history 영역으로 취급한다.
