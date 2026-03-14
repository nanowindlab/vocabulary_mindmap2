// 09_app_v2/src/data/loaderAdapter.js

const BASE_URL = import.meta.env.BASE_URL || "/";
const DATA_DIR = `${BASE_URL}data/`;

export async function loadCoreManifest() {
  const resp = await fetch(`${DATA_DIR}APP_READY_CORE_TREE_V1.json`);
  if (!resp.ok) throw new Error("Failed to load core manifest");
  return await resp.json();
}

export async function loadMetaManifest() {
  const resp = await fetch(`${DATA_DIR}APP_READY_META_TREE_V1.json`);
  if (!resp.ok) throw new Error("Failed to load meta manifest");
  return await resp.json();
}

export async function loadExpressionManifest() {
  const resp = await fetch(`${DATA_DIR}APP_READY_EXPRESSION_TREE_V1.json`);
  if (!resp.ok) throw new Error("Failed to load expression manifest");
  return await resp.json();
}

export async function loadEnglishMapping() {
  const resp = await fetch(`${DATA_DIR}ENGLISH_MAPPING_INVENTORY_V1.json`);
  if (!resp.ok) throw new Error("Failed to load english mapping");
  return await resp.json();
}

export async function loadSearchIndex() {
  const resp = await fetch(`${DATA_DIR}APP_READY_SEARCH_INDEX_V1.json`);
  if (!resp.ok) {
    console.warn("Search index not found, falling back to empty array");
    return [];
  }
  return await resp.json();
}

export async function loadTermDetailChunk(termId, chunkId) {
  if (!chunkId) return null;
  const resp = await fetch(`${DATA_DIR}APP_READY_CHUNK_RICH_${chunkId}.json`);
  if (!resp.ok) throw new Error(`Failed to load chunk ${chunkId}`);
  const chunkData = await resp.json();
  return chunkData.data[termId] || null;
}
