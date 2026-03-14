# REV47 Dev Handoff V1

> Date: `2026-03-12 09:50:11 KST`

- 핵심 변화량:
  - XWD 기반 relation mining 완료 후 의미 정책 재정렬
  - `linked_terms 7675`
  - `link_edges 28308`
  - 같은 `system/root/category`만 `related_vocab` 유지
  - 다른 분류 이동은 `refs.cross_links`로 분리
- live 파일별 `related_vocab`:
  - situations `4289`
  - expressions `1724`
  - basics `1618`
  - search `7631`
- live 파일별 `cross_links`:
  - situations `559`
  - expressions `100`
  - basics `146`
  - search `805`
- 주의점:
  - `self_link_count 0`
  - `asymmetry_sample_count 0`
  - `related_vocab`는 가까운 단어용, `refs.cross_links`는 다른 분류 점프용으로 해석할 것
  - `APP_READY_SEARCH_INDEX.json`의 `chunk_id`는 `8092 / 8092` 유지됨
