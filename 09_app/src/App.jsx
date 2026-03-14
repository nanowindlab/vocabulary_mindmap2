import React, { useState, useEffect, useMemo, useCallback, useRef } from "react";
import {
  Network, GalleryHorizontal, Loader, Book,
  Map as MapIcon, LayoutList, X, Filter, ChevronDown,
} from "lucide-react";

import { SidebarTree } from "./components/SidebarTree";
import { TermDetail } from "./components/TermDetail";
import { SearchBox } from "./components/SearchBox";
import { FlipcardDeck } from "./components/FlipcardDeck";
import { MindmapCanvas } from "./components/MindmapCanvas";
import {
  loadSituationsTree,
  loadExpressionsTree,
  loadBasicsTree,
  loadUnifiedSearchIndex,
  loadTermDetailChunk,
} from "./data/loaderAdapter";

import "./index.css";

// ── 3-축 탭 정의 ────────────────────────────────────────────────
const TABS = [
  { id: "situations", label: "상황과 장소", label_en: "Situations & Places", color: "#58a6ff" },
  { id: "expressions", label: "마음과 표현", label_en: "Heart & Expression",  color: "#3fb950" },
  { id: "basics",      label: "구조와 기초", label_en: "Structure & Basics",  color: "#bc8cff" },
];

// ── Band/Level 필터 옵션 ─────────────────────────────────────────
const BAND_OPTIONS  = [null, 1, 2, 3, 4, 5]; // null = 미산출 포함
const LEVEL_OPTIONS = ["all", "Beginner", "Intermediate", "Advanced", "Unrated"];

// ── 데이터 정규화 ────────────────────────────────────────────────
function normalizeItem(item, surface, idxMap = null) {
  const hier = item.hierarchy || {};
  const rootId   = hier.root_id   || hier.system || hier.root || null;
  const rootLabel= hier.root_label|| hier.system || hier.root || rootId || "";
  const scene    = hier.scene     || hier.root   || "일반";
  const category = hier.category  || item.pos    || "기타";

  // 방어 로직: Null/Undefined 방지 및 배열 필터링
  let related_vocab = Array.isArray(item.related_vocab) ? item.related_vocab.filter(Boolean) : [];
  let refs = item.refs && typeof item.refs === "object" ? item.refs : {};
  let cross_links = Array.isArray(refs.cross_links) ? refs.cross_links.filter(c => c && (c.target_id || c.target_term)) : [];

  // 검색 인덱스(idxMap) 존재 시, 양방향으로 빌드된 데이터(연관어 등) 병합 처리
  if (idxMap && item.id && idxMap.has(item.id)) {
    const idxEntry = idxMap.get(item.id);
    if (related_vocab.length === 0 && Array.isArray(idxEntry.related_vocab)) {
      related_vocab = idxEntry.related_vocab.filter(Boolean);
    }
    if (cross_links.length === 0 && idxEntry.refs && Array.isArray(idxEntry.refs.cross_links)) {
      cross_links = idxEntry.refs.cross_links.filter(c => c && (c.target_id || c.target_term));
    }
  }

  return {
    ...item,
    def_ko: item.def_ko || item.def_kr || "",
    phonetic_romanization: item.phonetic_romanization || item.roman || "",
    surface: surface || item.surface || "mindmap_core",
    routing: item.routing || surface || "mindmap_core",
    related_vocab,
    refs: {
      ...refs,
      cross_links,
    },
    hierarchy: {
      ...hier,
      root_id: rootId,
      root_label: rootLabel,
      root_en: hier.root_en || "",
      scene,
      category,
      path_ko: hier.path_ko || `${rootLabel} > ${scene} > ${category}`,
    },
  };
}

// ── 트리 빌더 ────────────────────────────────────────────────────
function buildTreeFromList(list, surface) {
  const tree = {};
  if (!Array.isArray(list)) return tree;
  list.forEach((rawItem) => {
    const item = normalizeItem(rawItem, surface);
    const rootId    = item.hierarchy?.root_id;
    const centerId  = item.hierarchy?.scene    || "일반";
    const categoryId= item.hierarchy?.category || item.pos || "기타";

    if (!rootId) return;
    if (!tree[rootId])
      tree[rootId] = { id: rootId, type: "root", label: item.hierarchy.root_label || rootId, label_en: item.hierarchy.root_en, children: {} };
    if (!tree[rootId].children[centerId])
      tree[rootId].children[centerId] = { id: centerId, type: "scene", label: centerId, children: {} };
    if (!tree[rootId].children[centerId].children[categoryId])
      tree[rootId].children[centerId].children[categoryId] = { id: categoryId, type: "category", label: categoryId, children: {} };
    if (!item.is_center_profile)
      tree[rootId].children[centerId].children[categoryId].children[item.id] = { id: item.id, type: "term", label: item.word, data: item };
  });
  return tree;
}

// ── 필터 함수 ────────────────────────────────────────────────────
function applyFilters(list, filters) {
  let result = list;
  if (filters.bands.length > 0) {
    result = result.filter((t) => {
      const b = t.stats?.band ?? null;
      return filters.bands.includes(b);
    });
  }
  if (filters.levels.length > 0) {
    result = result.filter((t) => filters.levels.includes(t.stats?.level || "Unrated"));
  }
  if (filters.poses && filters.poses.length > 0) {
    result = result.filter((t) => {
      const p = t.pos || t.part_of_speech || "미분류";
      // 선택된 품사 배열 중 하나라도 항목의 품사 문자열에 포함되면 통과
      return filters.poses.some((posFilter) => p.includes(posFilter));
    });
  }
  if (filters.query) {
    const q = filters.query.toLowerCase();
    result = result.filter((t) =>
      t.word?.includes(filters.query) ||
      t.def_ko?.includes(filters.query) ||
      t.def_en?.toLowerCase().includes(q)
    );
  }
  return result;
}

// ── 공통 컴포넌트: 드롭다운 필터 ──────────────────────────────────
const DropdownFilter = ({ label, options, selectedValues, onToggle, onClear }) => {
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const hasSelection = selectedValues.length > 0;

  return (
    <div ref={ref} style={{ position: "relative" }}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          display: "flex", alignItems: "center", gap: 6,
          padding: "6px 12px", borderRadius: 8, fontSize: 12, fontWeight: 600, cursor: "pointer",
          background: hasSelection ? "rgba(88,166,255,0.1)" : "rgba(255,255,255,0.05)",
          border: `1px solid ${hasSelection ? "var(--accent-blue)" : "var(--border-color)"}`,
          color: hasSelection ? "var(--accent-blue)" : "var(--text-secondary)",
          transition: "all 0.15s"
        }}
      >
        {label}
        {hasSelection && (
          <span style={{ background: "var(--accent-blue)", color: "#0d1117", padding: "1px 6px", borderRadius: 10, fontSize: 10 }}>
            {selectedValues.length}
          </span>
        )}
        <ChevronDown size={14} style={{ transform: isOpen ? "rotate(180deg)" : "none", transition: "transform 0.2s" }} />
      </button>

      {isOpen && (
        <div style={{
          position: "absolute", top: "100%", left: 0, marginTop: 8,
          background: "var(--bg-secondary)", border: "1px solid var(--border-color)",
          borderRadius: 8, padding: "8px", display: "flex", flexDirection: "column", gap: 4,
          minWidth: 160, zIndex: 100, boxShadow: "0 8px 24px rgba(0,0,0,0.5)"
        }}>
          {options.map((opt) => {
            const isSelected = selectedValues.includes(opt.value);
            return (
              <label key={opt.value} style={{
                display: "flex", alignItems: "center", gap: 8, padding: "6px 8px", borderRadius: 6,
                fontSize: 12, cursor: "pointer", transition: "background 0.1s",
                background: isSelected ? "rgba(255,255,255,0.05)" : "transparent",
                color: isSelected ? "var(--text-primary)" : "var(--text-secondary)"
              }}>
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => onToggle(opt.value)}
                  style={{ accentColor: "var(--accent-blue)", cursor: "pointer", width: 14, height: 14 }}
                />
                <span style={{ flex: 1 }}>{opt.label}</span>
                {opt.colorDot && (
                  <div style={{ width: 8, height: 8, borderRadius: "50%", background: opt.colorDot }} />
                )}
              </label>
            );
          })}
          {hasSelection && (
            <div style={{ marginTop: 4, paddingTop: 6, borderTop: "1px solid var(--border-color)", textAlign: "center" }}>
              <button
                onClick={onClear}
                style={{ background: "transparent", border: "none", color: "var(--text-secondary)", fontSize: 11, cursor: "pointer", padding: "4px" }}
              >
                초기화
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
// ── 메인 앱 ─────────────────────────────────────────────────────
function App() {
  const [activeTab, setActiveTab] = useState("situations");
  const [viewMode, setViewMode] = useState("mindmap");

  const [situationsList, setSituationsList] = useState([]);
  const [expressionsList, setExpressionsList] = useState([]);
  const [basicsList, setBasicsList] = useState([]);
  const [searchIndex, setSearchIndex] = useState([]);

  const [selectedTermDetail, setSelectedTermDetail] = useState(null);
  const [isLoadingChunk, setIsLoadingChunk] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);

  const [expandedIds, setExpandedIds] = useState(new Set());
  const [focusedRootId, setFocusedRootId] = useState(null);
  const [isFlipcardOpen, setIsFlipcardOpen] = useState(false);
  const [showEnglish, setShowEnglish] = useState(true);

  // 필터 상태
  const [filters, setFilters] = useState({ bands: [], levels: [], poses: [], query: "" });
  const [showFilterPanel, setShowFilterPanel] = useState(true);

  // 리사이저 상태
  const [detailWidth, setDetailWidth] = useState(45); // 초기 패널 너비(%)
  const isDragging = useRef(false);

  const startDrag = useCallback((e) => {
    isDragging.current = true;
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
  }, []);

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!isDragging.current) return;
      // 전체 컨테이너에서 사이드바(260px)를 제외한 영역 기준
      const containerWidth = window.innerWidth - 260; 
      const newWidth = ((containerWidth - (e.clientX - 260)) / containerWidth) * 100;
      if (newWidth >= 25 && newWidth <= 75) { // 25% ~ 75% 사이로 제한 (레이아웃 보호)
        setDetailWidth(newWidth);
      }
    };
    const handleMouseUp = () => {
      if (isDragging.current) {
        isDragging.current = false;
        document.body.style.cursor = "default";
        document.body.style.userSelect = "auto";
      }
    };
    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, []);

  // ── 데이터 로드 ─────────────────────────────────────────────────
  useEffect(() => {
    async function init() {
      try {
        setIsInitializing(true);
        const [sit, expr, bas, idx] = await Promise.all([
          loadSituationsTree(),
          loadExpressionsTree(),
          loadBasicsTree(),
          loadUnifiedSearchIndex(),
        ]);
        const searchIndexArr = Array.isArray(idx) ? idx : [];
        const idxMap = new Map();
        searchIndexArr.forEach((t) => { if (t.id) idxMap.set(t.id, t); });

        const sitArr  = Array.isArray(sit)  ? sit.map((t)  => normalizeItem(t, "mindmap_core", idxMap)) : [];
        const exprArr = Array.isArray(expr) ? expr.map((t) => normalizeItem(t, "expression_core", idxMap)) : [];
        const basArr  = Array.isArray(bas)  ? bas.map((t)  => normalizeItem(t, "mindmap_core", idxMap)) : [];
        
        setSituationsList(sitArr);
        setExpressionsList(exprArr);
        setBasicsList(basArr);
        setSearchIndex(searchIndexArr);

        if (sitArr.length > 0) {
          const defaultRoot = sitArr[0].hierarchy?.root_id;
          if (defaultRoot) {
            setFocusedRootId(defaultRoot);
            setExpandedIds(new Set([defaultRoot]));
          }
        }
      } catch (e) {
        console.error("데이터 로딩 실패", e);
      } finally {
        setIsInitializing(false);
      }
    }
    init();
  }, []);

  // ── 현재 축 데이터 ──────────────────────────────────────────────
  const activeList = useMemo(() => {
    if (activeTab === "situations")  return situationsList;
    if (activeTab === "expressions") return expressionsList;
    return basicsList;
  }, [activeTab, situationsList, expressionsList, basicsList]);

  const filteredList = useMemo(() => applyFilters(activeList, filters), [activeList, filters]);

  const activeSurface = activeTab === "expressions" ? "expression_core" : "mindmap_core";
  const activeTree = useMemo(() => buildTreeFromList(filteredList, activeSurface), [filteredList, activeSurface]);

  // ── 단어 선택 ───────────────────────────────────────────────────
  const handleSelectTerm = useCallback(async (term) => {
    if (!term?.id) return;
    setIsLoadingChunk(true);
    setSelectedTermDetail(term);

    // ── 사이드바 & 마인드맵 루트 상시 동기화: 선택 단어의 소속 노드를 강제 활성화 ──
    const rootId  = term.hierarchy?.root_id;
    const sceneId = term.hierarchy?.scene;
    const catId   = term.hierarchy?.category;
    
    if (rootId) {
      setFocusedRootId(rootId);
    }

    setExpandedIds((prev) => {
      const next = new Set(prev);
      if (sceneId) next.add(sceneId);
      if (catId)   next.add(catId);
      return next;
    });

    try {
      if (term.chunk_id) {
        const chunkData = await loadTermDetailChunk(term.id, term.chunk_id);
        if (chunkData)
          setSelectedTermDetail((prev) => prev?.id === term.id ? { ...prev, ...chunkData } : prev);
      } else {
        console.warn("[App] chunk_id missing for term:", term.id);
      }
    } catch (e) {
      console.warn(e);
    } finally {
      setIsLoadingChunk(false);
    }
  }, []);


  // ── 검색 선택 ───────────────────────────────────────────────────
  const handleSearchSelect = useCallback((target) => {
    const surface = target.surface || target.routing || "mindmap_core";
    if (surface === "expression_core") {
      setActiveTab("expressions");
    } else if (target.hierarchy?.system === "구조와 기초" || target.hierarchy?.root_id === "구조와 기초") {
      setActiveTab("basics");
    } else {
      setActiveTab("situations");
    }
    const normalized = normalizeItem(target, surface);
    handleSelectTerm(normalized);
    const rid = target.hierarchy?.root_id;
    if (rid) { setFocusedRootId(rid); setExpandedIds((prev) => new Set([...prev, rid])); }
  }, [handleSelectTerm]);

  // ── 필터 토글 ───────────────────────────────────────────────────
  const toggleBandFilter = (b) =>
    setFilters((f) => ({
      ...f,
      bands: f.bands.includes(b) ? f.bands.filter((x) => x !== b) : [...f.bands, b],
    }));

  const toggleLevelFilter = (lv) =>
    setFilters((f) => ({
      ...f,
      levels: f.levels.includes(lv) ? f.levels.filter((x) => x !== lv) : [...f.levels, lv],
    }));

  const togglePosFilter = (posKey) =>
    setFilters((f) => ({
      ...f,
      poses: (f.poses || []).includes(posKey) ? f.poses.filter((x) => x !== posKey) : [...(f.poses || []), posKey],
    }));

  const activeFilterCount = filters.bands.length + filters.levels.length + (filters.poses?.length || 0);

  // ── 연관 어휘 클릭 — 3대 축 횟단 점프 로직 ─────────────────────────────────
  // 자동 탭 전환 → 데이터 동기화 → 카테고리 Expand → Zoom-to-node
  const SYSTEM_TO_TAB = {
    "상황과 장소": "situations",
    "마음과 표현": "expressions",
    "구조와 기초": "basics",
  };

  const handleRelatedVocabClick = useCallback((wordString) => {
    const target = searchIndex.find((x) => x.word === wordString);
    if (!target) {
      console.warn("[RelatedVocab] 검색 인덱스 미존재:", wordString);
      return;
    }
    // handleSearchSelect로 통일: 탭/focusedRootId/expandedIds/마인드맵이 모두 함께 동기화됨
    handleSearchSelect(target);
  }, [searchIndex, handleSearchSelect]);

  // ── 플립카드 데이터 ─────────────────────────────────────────────
  const getFlipcardItems = () => {
    const pool = filteredList.filter((t) => t.word && t.def_ko);
    let deck = [];
    if (selectedTermDetail && pool.find((t) => t.id === selectedTermDetail.id))
      deck.push(selectedTermDetail);
    const extra = pool
      .filter((t) => t.id !== selectedTermDetail?.id)
      .sort(() => 0.5 - Math.random())
      .slice(0, 20 - deck.length);
    return {
      items: [...deck, ...extra],
      contextLabel: selectedTermDetail ? `'${selectedTermDetail.word}' 연관 학습` : "오늘의 무작위 학습",
    };
  };

  // ── 로딩 ────────────────────────────────────────────────────────
  if (isInitializing)
    return (
      <div className="welcome-screen">
        <Loader className="spinner" size={48} />
        <p>어휘 데이터 준비 중… ({TABS.map((t) => t.label).join(" · ")})</p>
      </div>
    );

  const currentTab = TABS.find((t) => t.id === activeTab);

  return (
    <div className="app-root fade-enter-active">
      {/* ── 상단 내비게이션 ─────────────────────────────────── */}
      <div className="top-nav">
        <div className="nav-left">
          <div className="logo">
            <Network size={24} color="var(--accent-blue)" />
            <span className="logo-text">어휘 마인드맵</span>
          </div>
          <div className="nav-tabs">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                className={`nav-tab ${activeTab === tab.id ? "active" : ""}`}
                onClick={() => { setActiveTab(tab.id); setSelectedTermDetail(null); setFocusedRootId(null); }}
                style={{ "--tab-color": tab.color }}
              >
                {tab.label}
                {activeTab === tab.id && (
                  <span style={{ fontSize: 11, opacity: 0.7, marginLeft: 6 }}>
                    ({filteredList.length.toLocaleString()})
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>

        <div className="nav-right">
          {/* ENG 토글 */}
          <button
            className="card-glass"
            onClick={() => setShowEnglish(!showEnglish)}
            style={{
              display: "flex", alignItems: "center", gap: 6,
              padding: "6px 12px", borderRadius: 8, cursor: "pointer", fontSize: 12,
              border: `1px solid ${showEnglish ? "var(--accent-blue)" : "var(--border-color)"}`,
              color: showEnglish ? "var(--accent-blue)" : "var(--text-secondary)",
            }}
          >
            <Book size={14} /> {showEnglish ? "ENG ON" : "ENG OFF"}
          </button>

          {/* 필터 버튼 */}
          <button
            className="card-glass"
            onClick={() => setShowFilterPanel(!showFilterPanel)}
            style={{
              display: "flex", alignItems: "center", gap: 6,
              padding: "6px 12px", borderRadius: 8, cursor: "pointer", fontSize: 12,
              border: `1px solid ${activeFilterCount > 0 ? "var(--accent-orange)" : "var(--border-color)"}`,
              color: activeFilterCount > 0 ? "var(--accent-orange)" : "var(--text-secondary)",
              position: "relative",
            }}
          >
            <Filter size={14} />
            필터 {activeFilterCount > 0 && <span style={{ background: "var(--accent-orange)", color: "#0d1117", borderRadius: 10, padding: "1px 5px", fontSize: 10, fontWeight: 700 }}>{activeFilterCount}</span>}
            <ChevronDown size={12} style={{ transform: showFilterPanel ? "rotate(180deg)" : "none", transition: "transform 0.2s" }} />
          </button>

          <SearchBox searchIndex={searchIndex} onSelect={handleSearchSelect} showEnglish={showEnglish} />

          {/* 카드 학습 */}
          <button
            onClick={() => { setSelectedTermDetail(null); setIsFlipcardOpen(true); }}
            style={{
              display: "flex", alignItems: "center", gap: 8, padding: "8px 16px",
              borderRadius: 8, backgroundColor: "var(--accent-green)", color: "#111",
              border: "none", cursor: "pointer", fontWeight: 600, fontSize: 13,
            }}
          >
            <GalleryHorizontal size={16} /> 카드 학습
          </button>
        </div>
      </div>

      {/* ── 필터 패널 ─────────────────────────────────────────── */}
      {showFilterPanel && (
        <div style={{
          background: "var(--bg-secondary)", borderBottom: "1px solid var(--border-color)",
          padding: "12px 24px", display: "flex", gap: 16, alignItems: "center", flexWrap: "wrap",
        }}>
          {/* 드롭다운 필터 요소들 */}
          <DropdownFilter
            label="Band별"
            options={[
              { value: 1, label: "Band 1 (최상위 필수)", colorDot: "#ff7b72" },
              { value: 2, label: "Band 2 (핵심 중요)", colorDot: "#ffa657" },
              { value: 3, label: "Band 3 (일반 활용)", colorDot: "#e3b341" },
              { value: 4, label: "Band 4 (보조 표현)", colorDot: "#3fb950" },
              { value: 5, label: "Band 5 (심화 어휘)", colorDot: "#58a6ff" },
              { value: null, label: "미산출", colorDot: "#6e7681" },
            ]}
            selectedValues={filters.bands}
            onToggle={toggleBandFilter}
            onClear={() => setFilters(f => ({ ...f, bands: [] }))}
          />

          <DropdownFilter
            label="레벨별"
            options={[
              { value: "Beginner",     label: "초급" },
              { value: "Intermediate", label: "중급" },
              { value: "Advanced",     label: "고급" },
              { value: "Unrated",      label: "미산출" },
            ]}
            selectedValues={filters.levels}
            onToggle={toggleLevelFilter}
            onClear={() => setFilters(f => ({ ...f, levels: [] }))}
          />

          <DropdownFilter
            label="품사별"
            options={[
              "명사", "동사", "형용사", "부사", "대명사", "관형사", "수사", "감탄사", "조사", "접사", "구"
            ].map(pos => ({ value: pos, label: pos }))}
            selectedValues={filters.poses || []}
            onToggle={togglePosFilter}
            onClear={() => setFilters(f => ({ ...f, poses: [] }))}
          />

          {/* 모든 필터 초기화 버튼 */}
          {activeFilterCount > 0 && (
            <button onClick={() => setFilters({ bands: [], levels: [], poses: [], query: "" })}
              style={{ padding: "6px 12px", borderRadius: 8, fontSize: 12, fontWeight: 600, cursor: "pointer", color: "var(--accent-orange)", background: "rgba(255,166,87,0.1)", border: "1px solid rgba(255,166,87,0.3)", transition: "all 0.15s" }}>
              전체 필터 초기화
            </button>
          )}

          <span style={{ fontSize: 12, color: "var(--text-secondary)", marginLeft: "auto" }}>
            {filteredList.length.toLocaleString()} / {activeList.length.toLocaleString()}건 표시 중
          </span>
        </div>
      )}

      {/* ── 메인 콘텐츠 ───────────────────────────────────────── */}
      <div className="app-container">
        <SidebarTree
          treeData={activeTree}
          expandedIds={expandedIds}
          toggleExpand={(id) =>
            setExpandedIds((prev) => {
              const n = new Set(prev);
              if (n.has(id)) n.delete(id); else n.add(id);
              return n;
            })
          }
          onSelectTerm={handleSelectTerm}
          selectedTermId={selectedTermDetail?.id}
        />

        <div className="main-content">
          {/* 뷰 전환 바 */}
          <div style={{
            padding: "12px 24px", borderBottom: "1px solid var(--border-color)",
            backgroundColor: "var(--bg-secondary)", display: "flex",
            justifyContent: "space-between", alignItems: "center",
          }}>
            <div style={{ fontWeight: 600, fontSize: 15, color: currentTab?.color || "var(--text-primary)" }}>
              {currentTab?.label}
              {currentTab?.label_en && <span style={{ fontSize: 12, color: "var(--text-secondary)", marginLeft: 8 }}>{currentTab.label_en}</span>}
            </div>
            <div style={{ display: "flex", gap: 8, backgroundColor: "var(--bg-tertiary)", padding: 4, borderRadius: 8, border: "1px solid var(--border-color)" }}>
              {[
                { mode: "mindmap", icon: <MapIcon size={14} />, label: "마인드맵" },
                { mode: "list",    icon: <LayoutList size={14} />, label: "리스트" },
              ].map(({ mode, icon, label }) => (
                <button key={mode}
                  style={{
                    display: "flex", alignItems: "center", gap: 6, padding: "6px 12px",
                    borderRadius: 6, cursor: "pointer", fontSize: 13,
                    border: viewMode === mode ? "1px solid var(--border-color)" : "1px solid transparent",
                    backgroundColor: viewMode === mode ? "var(--bg-secondary)" : "transparent",
                    color: viewMode === mode ? "var(--text-primary)" : "var(--text-secondary)",
                    transition: "all 0.15s",
                  }}
                  onClick={() => setViewMode(mode)}
                >{icon} {label}</button>
              ))}
            </div>
          </div>

          <div style={{ flex: 1, display: "flex", overflow: "hidden" }}>
            {/* 뷰 영역 */}
            <div style={{
              flex: selectedTermDetail ? `1 1 ${100 - detailWidth}%` : "1",
              overflow: "hidden",
            }}>
              {viewMode === "mindmap" ? (
                <MindmapCanvas
                  treeData={activeTree}
                  onSelectTerm={handleSelectTerm}
                  selectedTermId={selectedTermDetail?.id}
                  focusedRootId={focusedRootId}
                />
              ) : (
                <ListView
                  list={filteredList}
                  selectedTermId={selectedTermDetail?.id}
                  onSelectTerm={handleSelectTerm}
                  showEnglish={showEnglish}
                />
              )}
            </div>

            {/* Splitter (가변 조절바) */}
            {selectedTermDetail && (
              <div
                onMouseDown={startDrag}
                style={{
                  width: 10,
                  cursor: "col-resize",
                  backgroundColor: "transparent",
                  zIndex: 50,
                  position: "relative",
                  marginLeft: -5,
                  marginRight: -5,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <div
                  style={{
                    width: 4,
                    height: "100%",
                    backgroundColor: "var(--border-color)",
                    transition: "background-color 0.2s",
                  }}
                  onMouseEnter={(e) => (e.target.style.backgroundColor = "var(--accent-blue)")}
                  onMouseLeave={(e) => {
                    if (!isDragging.current) e.target.style.backgroundColor = "var(--border-color)";
                  }}
                />
              </div>
            )}

            {/* 상세 패널 */}
            {selectedTermDetail && (
              <div style={{
                flex: `0 0 ${detailWidth}%`,
                borderLeft: "1px solid var(--border-color)",
                backgroundColor: "var(--bg-primary)", display: "flex", flexDirection: "column",
                minWidth: 300,
              }}>
                <div style={{
                  padding: "10px 16px", borderBottom: "1px solid var(--border-color)",
                  backgroundColor: "var(--bg-secondary)", display: "flex", alignItems: "center", gap: 8, justifyContent: "flex-end",
                }}>
                  <button onClick={() => setIsFlipcardOpen(true)}
                    style={{ padding: "6px 12px", backgroundColor: "rgba(63,185,80,0.1)", border: "1px solid var(--accent-green)", color: "var(--accent-green)", borderRadius: 6, cursor: "pointer", fontSize: 12, fontWeight: 600 }}>
                    카드 학습
                  </button>
                  <button onClick={() => setSelectedTermDetail(null)}
                    style={{ padding: "6px 12px", backgroundColor: "var(--bg-secondary)", border: "1px solid var(--border-color)", color: "var(--text-secondary)", borderRadius: 6, cursor: "pointer", fontSize: 12 }}>
                    <X size={14} style={{ display: "inline", verticalAlign: "middle" }} /> 닫기
                  </button>
                </div>
                <div style={{ flex: 1, overflowY: "auto" }}>
                  {isLoadingChunk ? (
                    <div className="welcome-screen"><Loader className="spinner" /><p>로딩 중...</p></div>
                  ) : (
                    <TermDetail
                      term={selectedTermDetail}
                      siblingSenses={[]}
                      onSenseSwitch={handleSelectTerm}
                      onCrossLinkClick={(link) => {
                        // target_id 기반 정확 매칭 (새 canonical 데이터 기준)
                        let target = null;
                        if (link.target_id) {
                          target = searchIndex.find((x) => x.id === link.target_id);
                        }
                        // fallback: target_term으로만 찾기 (구버전 데이터 대비)
                        if (!target && link.target_term) {
                          target = searchIndex.find((x) => x.word === link.target_term);
                        }

                        if (target && target.id !== selectedTermDetail?.id) {
                          handleSearchSelect(target);
                        } else {
                          console.warn("[CrossLink] 점프 불가:", link);
                        }
                      }}
                      onRelatedVocabClick={handleRelatedVocabClick}
                      showEnglish={showEnglish}
                    />
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 플립카드 */}
      {isFlipcardOpen && (
        <FlipcardDeck
          items={getFlipcardItems().items}
          contextLabel={getFlipcardItems().contextLabel}
          onClose={() => setIsFlipcardOpen(false)}
          showEnglish={showEnglish}
        />
      )}
    </div>
  );
}

// ── 리스트 뷰 ────────────────────────────────────────────────────
const BAND_COLORS_INLINE = {
  1: { color: "#ff7b72", bg: "rgba(255,123,114,0.12)", label: "Essential" },
  2: { color: "#ffa657", bg: "rgba(255,166,87,0.12)",  label: "High"      },
  3: { color: "#e3b341", bg: "rgba(227,179,65,0.12)",  label: "Medium"    },
  4: { color: "#3fb950", bg: "rgba(63,185,80,0.12)",   label: "Low"       },
  5: { color: "#58a6ff", bg: "rgba(88,166,255,0.12)",  label: "Rare"      },
};

function ListView({ list, selectedTermId, onSelectTerm, showEnglish }) {
  return (
    <div style={{ padding: 16, overflowY: "auto", height: "100%" }}>
      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
        {list.map((term) => {
          const band = term.stats?.band ?? null;
          const bandValid = band !== null && band >= 1 && band <= 5;
          const bm = bandValid ? BAND_COLORS_INLINE[band] : null;
          const isSelected = selectedTermId === term.id;

          return (
            <div
              key={term.id}
              onClick={() => onSelectTerm(term)}
              style={{
                padding: "10px 16px", borderRadius: 10, cursor: "pointer",
                backgroundColor: isSelected ? "rgba(47,129,247,0.12)" : "var(--bg-secondary)",
                border: `1px solid ${isSelected ? "var(--accent-blue)" : "var(--border-color)"}`,
                display: "flex", alignItems: "center", gap: 12, transition: "all 0.12s",
              }}
            >
              <span style={{ fontWeight: 600, color: isSelected ? "var(--accent-blue)" : "var(--text-primary)", fontSize: 14 }}>
                {term.word}
              </span>
              {showEnglish && term.def_en && (
                <span style={{ color: "var(--text-secondary)", fontSize: 12, flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {term.def_en}
                </span>
              )}
              <div style={{ display: "flex", gap: 6, marginLeft: "auto", flexShrink: 0 }}>
                {bm ? (
                  <span style={{ fontSize: 10, fontWeight: 600, padding: "2px 7px", borderRadius: 6, background: bm.bg, color: bm.color, border: `1px solid ${bm.color}44` }}>
                    B{band}
                  </span>
                ) : (
                  <span style={{ fontSize: 10, color: "#6e7681", padding: "2px 7px", borderRadius: 6, background: "rgba(110,118,129,0.1)", border: "1px solid rgba(110,118,129,0.2)" }}>
                    —
                  </span>
                )}
                {term.stats?.level && term.stats.level !== "Unrated" && (
                  <span style={{ fontSize: 10, color: "var(--text-secondary)", padding: "2px 7px", borderRadius: 6, border: "1px solid var(--border-color)" }}>
                    {term.stats.level === "Beginner" ? "초" : term.stats.level === "Intermediate" ? "중" : "고"}
                  </span>
                )}
              </div>
            </div>
          );
        })}
        {list.length === 0 && (
          <div style={{ textAlign: "center", color: "var(--text-secondary)", padding: "60px 20px" }}>
            해당 조건의 단어가 없습니다.
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
