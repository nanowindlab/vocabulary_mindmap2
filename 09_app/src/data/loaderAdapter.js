// loaderAdapter.js  – V2 (2026-03-11)
// 신 스키마 파일 기준:
//   APP_READY_SITUATIONS_TREE.json   → Array<item>  (상황과 장소, 4,541건)
//   APP_READY_EXPRESSIONS_TREE.json  → Array<item>  (마음과 표현, 1,829건)
//   APP_READY_BASICS_TREE.json       → Array<item>  (구조와 기초, 1,722건)
//   APP_READY_SEARCH_INDEX.json      → Array<item>  (8,092건 통합)
//
// 레거시 호환:
//   APP_READY_CHUNK_RICH_*           → {[termId]: {...}}
//   APP_READY_CHUNK_EXAMPLES_*       → { chunk_id, data: {[termId]: {...}} }

const BASE_URL = import.meta.env.BASE_URL || "/";
const DATA_DIR = `${BASE_URL}data/`;
const LIVE_DIR = `${DATA_DIR}live/`;
const LEGACY_DIR = `${DATA_DIR}legacy/`;

// ── 3-축 분리 로더 (신규) ───────────────────────────────────────────────
export async function loadSituationsTree() {
  const resp = await fetch(`${LIVE_DIR}APP_READY_SITUATIONS_TREE.json`);
  if (!resp.ok) throw new Error("Failed to load situations tree");
  return await resp.json();
}

export async function loadExpressionsTree() {
  const resp = await fetch(`${LIVE_DIR}APP_READY_EXPRESSIONS_TREE.json`);
  if (!resp.ok) throw new Error("Failed to load expressions tree");
  return await resp.json();
}

export async function loadBasicsTree() {
  const resp = await fetch(`${LIVE_DIR}APP_READY_BASICS_TREE.json`);
  if (!resp.ok) throw new Error("Failed to load basics tree");
  return await resp.json();
}

export async function loadUnifiedSearchIndex() {
  const resp = await fetch(`${LIVE_DIR}APP_READY_SEARCH_INDEX.json`);
  if (!resp.ok) {
    console.warn("Unified search index not found, falling back to V1");
    return loadSearchIndex();
  }
  return await resp.json();
}

// ── 레거시 호환 로더 ───────────────────────────────────────────────────
export async function loadCoreManifest() {
  const resp = await fetch(`${LEGACY_DIR}APP_READY_CORE_TREE_V1.json`);
  if (!resp.ok) throw new Error("Failed to load core manifest");
  return await resp.json();
}

export async function loadMetaManifest() {
  const resp = await fetch(`${LEGACY_DIR}APP_READY_META_TREE_V1.json`);
  if (!resp.ok) throw new Error("Failed to load meta manifest");
  return await resp.json();
}

export async function loadExpressionManifest() {
  const resp = await fetch(`${LEGACY_DIR}APP_READY_EXPRESSION_TREE_V1.json`);
  if (!resp.ok) throw new Error("Failed to load expression manifest");
  return await resp.json();
}

export async function loadEnglishMapping() {
  try {
    const resp = await fetch(`${LIVE_DIR}ENGLISH_MAPPING_INVENTORY_V1.json`);
    if (!resp.ok) return null;
    return await resp.json();
  } catch {
    return null;
  }
}

export async function loadSearchIndex() {
  const resp = await fetch(`${LEGACY_DIR}APP_READY_SEARCH_INDEX_V1.json`);
  if (!resp.ok) {
    console.warn("Search index not found, falling back to empty array");
    return [];
  }
  return await resp.json();
}

/**
 * 단어 상세 데이터를 RICH chunk + EXAMPLES chunk 에서 합산하여 반환한다.
 */
export async function loadTermDetailChunk(termId, chunkId) {
  if (!termId || !chunkId) return null;

  const [richResp, examplesResp] = await Promise.allSettled([
    fetch(`${LIVE_DIR}APP_READY_CHUNK_RICH_${chunkId}.json`),
    fetch(`${LIVE_DIR}APP_READY_CHUNK_EXAMPLES_${chunkId}.json`),
  ]);

  let richEntry = null;
  let examplesEntry = null;

  if (richResp.status === "fulfilled" && richResp.value.ok) {
    try {
      const richData = await richResp.value.json();
      richEntry = richData[termId] || null;
    } catch (e) {
      console.warn("[loaderAdapter] RICH chunk parse error:", e);
    }
  }

  if (examplesResp.status === "fulfilled" && examplesResp.value.ok) {
    try {
      const exData = await examplesResp.value.json();
      examplesEntry = (exData.data || {})[termId] || null;
    } catch (e) {
      console.warn("[loaderAdapter] EXAMPLES chunk parse error:", e);
    }
  }

  if (!richEntry && !examplesEntry) return null;

  let examples_bundle = [];
  if (examplesEntry?.attested_sentences) {
    examples_bundle = examplesEntry.attested_sentences
      .filter((s) => s.ko && s.ko.length > 5)
      .slice(0, 8)
      .map((s) => ({
        text_ko: s.ko,
        text_en: s.en || null,
        source: s.round ? `TOPIK ${s.round}` : null,
      }));
  }

  return {
    ...(richEntry || {}),
    related_vocab:
      richEntry?.related_vocab || examplesEntry?.related_vocab || [],
    examples_bundle,
    phonetic_romanization:
      examplesEntry?.phonetic_romanization ||
      richEntry?.phonetic_romanization ||
      null,
  };
}
