import React, { useState, useEffect, useMemo, useCallback } from "react";
import {
  Network, GraduationCap, Compass, Loader, Search, Map as MapIcon,
  LayoutList, GalleryHorizontal, PlayCircle, Clock, ExternalLink, X, Book
} from "lucide-react";

import { SidebarTree } from "./components/SidebarTree";
import { TermDetail } from "./components/TermDetail";
import { MetaLearningBoard } from "./components/MetaLearningBoard";
import { ExpressionBoard } from "./components/ExpressionBoard";
import { SearchBox } from "./components/SearchBox";
import { FlipcardDeck } from "./components/FlipcardDeck";
import { MindmapCanvas } from "./components/MindmapCanvas";
import {
  loadCoreManifest, loadTermDetailChunk, loadMetaManifest,
  loadExpressionManifest, loadEnglishMapping, loadSearchIndex,
} from "./data/loaderAdapter";

import "./index.css";

// 헬퍼: 평탄한 배열 데이터를 트리 구조(Object)로 변환
function buildTreeFromList(list) {
  const tree = {};
  if (!Array.isArray(list)) return tree;
  list.forEach(item => {
    const { root_id, center_id, category_id } = item.hierarchy || {};
    if (!root_id) return;
    if (!tree[root_id]) tree[root_id] = { id: root_id, type: 'root', label: root_id, children: {} };
    if (center_id) {
      if (!tree[root_id].children[center_id]) tree[root_id].children[center_id] = { id: center_id, type: 'scene', label: center_id, children: {} };
      if (category_id) {
        if (!tree[root_id].children[center_id].children[category_id]) tree[root_id].children[center_id].children[category_id] = { id: category_id, type: 'category', label: category_id, children: {} };
        tree[root_id].children[center_id].children[category_id].children[item.id] = { id: item.id, type: 'term', label: item.word, data: item };
      }
    }
  });
  return tree;
}

function App() {
  const [activeTab, setActiveTab] = useState("core");
  const [coreViewMode, setCoreViewMode] = useState("mindmap");
  const [metaViewMode, setMetaViewMode] = useState("list");
  const [exprViewMode, setExprViewMode] = useState("list");

  const [coreList, setCoreList] = useState([]);
  const [metaList, setMetaList] = useState([]);
  const [expressionList, setExpressionList] = useState([]);
  const [englishMapping, setEnglishMapping] = useState(null);
  const [searchIndex, setSearchIndex] = useState([]);

  const [selectedTermDetail, setSelectedTermDetail] = useState(null);
  const [isLoadingChunk, setIsLoadingChunk] = useState(false);
  const [errorState, setErrorState] = useState(null);
  const [isInitializing, setIsInitializing] = useState(true);

  const [expandedIds, setExpandedIds] = useState(new Set());
  const [focusedRootId, setFocusedRootId] = useState(null);
  const [isFlipcardOpen, setIsFlipcardOpen] = useState(false);
  const [showEnglish, setShowEnglish] = useState(true);

  useEffect(() => {
    async function init() {
      try {
        setIsInitializing(true);
        const [core, meta, expr, mapping, idx] = await Promise.all([
          loadCoreManifest(), loadMetaManifest(), loadExpressionManifest(),
          loadEnglishMapping(), loadSearchIndex(),
        ]);
        setCoreList(Array.isArray(core) ? core : []);
        setMetaList(Array.isArray(meta) ? meta : []);
        setExpressionList(Array.isArray(expr) ? expr : []);
        setEnglishMapping(mapping);
        setSearchIndex(Array.isArray(idx) ? idx : []);
        if (Array.isArray(core) && core.length > 0) {
          const rootId = core[0].hierarchy?.root_id || "G01_FAMILY";
          setFocusedRootId(rootId);
          setExpandedIds(new Set([rootId]));
        }
      } catch (e) { setErrorState("데이터 로딩 실패"); }
      finally { setIsInitializing(false); }
    }
    init();
  }, []);

  const coreTree = useMemo(() => buildTreeFromList(coreList), [coreList]);

  const handleSelectTerm = async (term) => {
    if (!term || !term.id) return;
    setIsLoadingChunk(true);
    setSelectedTermDetail(term);
    try {
      const chunkData = await loadTermDetailChunk(term.id, term.chunk_id);
      if (chunkData) setSelectedTermDetail(prev => (prev?.id === term.id ? { ...prev, ...chunkData } : prev));
    } catch (e) { console.warn(e); }
    finally { setIsLoadingChunk(false); }
  };

  const handleCrossLinkClick = (link) => {
    const found = searchIndex.find(t => t.id === link.target_id || t.word === link.target_term);
    if (found) handleSearchSelect(found);
  };

  const handleSearchSelect = (target) => {
    const routing = target.routing || target.surface;
    if (routing?.includes("meta")) { setActiveTab("meta"); handleSelectTerm(target); }
    else if (routing?.includes("expression")) { setActiveTab("expression"); handleSelectTerm(target); }
    else {
      setActiveTab("core"); handleSelectTerm(target);
      const rid = target.hierarchy?.root_id;
      if (rid) { setFocusedRootId(rid); setExpandedIds(prev => new Set([...prev, rid])); }
    }
  };

  const getSiblingSenses = (term) => {
    if (!term?.homonym_group_id) return [];
    return [...coreList, ...metaList, ...expressionList].filter(t => t.homonym_group_id === term.homonym_group_id);
  };

  const getFlipcardItems = () => {
    const pool = [...coreList, ...expressionList].filter(t => t.word && t.def_ko && t.routing !== "meta_learning");
    let deck = [];
    if (selectedTermDetail && pool.find(t => t.id === selectedTermDetail.id)) deck.push(selectedTermDetail);
    const extra = pool.filter(t => t.id !== selectedTermDetail?.id).sort(() => 0.5 - Math.random()).slice(0, 20 - deck.length);
    return { items: [...deck, ...extra], contextLabel: selectedTermDetail ? `'${selectedTermDetail.word}' 연관` : "전체 학습" };
  };

  if (isInitializing) return <div className="welcome-screen"><Loader className="spinner" /><p>로딩 중...</p></div>;

  return (
    <div className="app-root">
      <div className="top-nav">
        <div className="nav-left">
          <div className="logo"><Network size={24} color="var(--accent-blue)" /><span className="logo-text">MindMap Explorer</span></div>
          <div className="nav-tabs">
            {['core', 'expression', 'meta'].map(tab => (
              <button key={tab} className={`nav-tab ${activeTab === tab ? "active" : ""}`} onClick={() => setActiveTab(tab)}>
                {tab === 'core' ? '장면별 단어' : tab === 'expression' ? '표현 코어' : '메타 학습'}
              </button>
            ))}
          </div>
        </div>
        <div className="nav-right">
          <button 
            className={`toggle-en-btn ${!showEnglish ? 'off' : ''}`}
            onClick={() => setShowEnglish(!showEnglish)}
            style={{
              marginRight: 12, padding: "6px 12px", borderRadius: 8, cursor: "pointer", fontSize: 12, display: "flex", alignItems: "center", gap: 6,
              border: `1px solid ${showEnglish ? 'var(--accent-blue)' : 'var(--border-color)'}`,
              backgroundColor: showEnglish ? 'rgba(47, 129, 247, 0.1)' : 'transparent',
              color: showEnglish ? 'var(--accent-blue)' : 'var(--text-secondary)',
            }}
          >
            <Book size={14} /> {showEnglish ? "ENG ON" : "ENG OFF"}
          </button>
          <SearchBox searchIndex={searchIndex} onSelect={handleSearchSelect} englishMapping={englishMapping} showEnglish={showEnglish} />
          <button className="today-card-btn" onClick={() => { setSelectedTermDetail(null); setIsFlipcardOpen(true); }}><GalleryHorizontal size={18} /> 학습 카드</button>
        </div>
      </div>

      <div className="app-container">
        {activeTab === "core" ? (
          <>
            <SidebarTree treeData={coreTree} expandedIds={expandedIds} toggleExpand={id => setExpandedIds(prev => { const n = new Set(prev); if (n.has(id)) n.delete(id); else n.add(id); return n; })} onSelectTerm={handleSelectTerm} selectedTermId={selectedTermDetail?.id} />
            <div className="main-content">
              <ViewSwitcher label="코어 확장 맵" icon={<Network size={16} color="var(--accent-blue)" />} viewMode={coreViewMode} setViewMode={setCoreViewMode} accentColor="var(--accent-blue)" />
              <div style={{ flex: 1, display: "flex", overflow: "hidden" }}>
                <div style={{ flex: selectedTermDetail ? "0 0 55%" : "1", borderRight: selectedTermDetail ? "1px solid var(--border-color)" : "none", overflow: "hidden" }}>
                  {coreViewMode === "mindmap" ? <MindmapCanvas treeData={coreTree} onSelectTerm={handleSelectTerm} onCrossLinkClick={handleCrossLinkClick} selectedTermId={selectedTermDetail?.id} focusedRootId={focusedRootId} /> : (
                    <div style={{ overflowY: "auto", height: "100%", padding: "16px" }}>
                      {coreList.map(term => <CoreListItem key={term.id} term={term} isSelected={selectedTermDetail?.id === term.id} onClick={() => handleSelectTerm(term)} showEnglish={showEnglish} />)}
                    </div>
                  )}
                </div>
                {selectedTermDetail && <DetailPanel surfaceLabel="코어 확장 맵" surfaceIcon={<Network size={14} color="var(--accent-blue)" />} surfaceColor="var(--accent-blue)" term={selectedTermDetail} siblingSenses={getSiblingSenses(selectedTermDetail)} englishMapping={englishMapping} isLoading={isLoadingChunk} onClose={() => setSelectedTermDetail(null)} onSenseSwitch={handleSelectTerm} onCrossLinkClick={handleCrossLinkClick} onRelatedVocabClick={handleSelectTerm} onFlipcardOpen={() => setIsFlipcardOpen(true)} showEnglish={showEnglish} />}
              </div>
            </div>
          </>
        ) : (
          <div className="main-content">
            <ViewSwitcher label={activeTab === 'expression' ? "표현 코어" : "메타 학습"} icon={<Compass size={16} color="var(--accent-orange)" />} viewMode={activeTab === 'expression' ? exprViewMode : metaViewMode} setViewMode={activeTab === 'expression' ? setExprViewMode : setMetaViewMode} accentColor="var(--accent-orange)" />
            <div style={{ flex: 1, display: "flex", overflow: "hidden" }}>
              <div style={{ flex: selectedTermDetail ? "0 0 55%" : "1", overflowY: "auto" }}>
                {activeTab === 'expression' ? <ExpressionBoard onExpressionItemClick={handleSelectTerm} selectedItemId={selectedTermDetail?.id} englishMapping={englishMapping} /> : <MetaLearningBoard onMetaItemClick={handleSelectTerm} selectedItemId={selectedTermDetail?.id} />}
              </div>
              {selectedTermDetail && <DetailPanel surfaceLabel={activeTab === 'expression' ? "표현 코어" : "메타 학습"} surfaceIcon={<Compass size={14} color="var(--accent-orange)" />} surfaceColor="var(--accent-orange)" term={selectedTermDetail} siblingSenses={getSiblingSenses(selectedTermDetail)} englishMapping={englishMapping} isLoading={isLoadingChunk} onClose={() => setSelectedTermDetail(null)} onSenseSwitch={handleSelectTerm} onCrossLinkClick={handleCrossLinkClick} onRelatedVocabClick={handleSelectTerm} onFlipcardOpen={() => setIsFlipcardOpen(true)} showEnglish={showEnglish} />}
            </div>
          </div>
        )}
      </div>
      {isFlipcardOpen && <FlipcardDeck items={getFlipcardItems().items} contextLabel={getFlipcardItems().contextLabel} onClose={() => setIsFlipcardOpen(false)} englishMapping={englishMapping} showEnglish={showEnglish} />}
    </div>
  );
}

function ViewSwitcher({ label, icon, viewMode, setViewMode, accentColor }) {
  const btnStyle = mode => ({
    display: "flex", alignItems: "center", gap: 6, padding: "6px 14px", borderRadius: 8, cursor: "pointer", fontSize: 13,
    fontWeight: viewMode === mode ? "bold" : "normal", backgroundColor: viewMode === mode ? accentColor : "var(--bg-secondary)",
    color: viewMode === mode ? "#fff" : "var(--text-secondary)", border: viewMode === mode ? `1px solid ${accentColor}` : "1px solid var(--border-color)",
  });
  return (
    <div style={{ padding: "10px 20px", borderBottom: "1px solid var(--border-color)", backgroundColor: "var(--bg-secondary)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>{icon}<span style={{ fontWeight: "bold", fontSize: 15 }}>{label}</span></div>
      <div style={{ display: "flex", gap: 8 }}>
        <button style={btnStyle("mindmap")} onClick={() => setViewMode("mindmap")}><MapIcon size={14} /> 마인드맵</button>
        <button style={btnStyle("list")} onClick={() => setViewMode("list")}><LayoutList size={14} /> 리스트</button>
      </div>
    </div>
  );
}

function DetailPanel({ surfaceLabel, surfaceIcon, surfaceColor, term, siblingSenses, englishMapping, isLoading, onClose, onSenseSwitch, onCrossLinkClick, onRelatedVocabClick, onFlipcardOpen, showEnglish }) {
  return (
    <div style={{ flex: "0 0 45%", borderLeft: "1px solid var(--border-color)", backgroundColor: "var(--bg-primary)", display: "flex", flexDirection: "column" }}>
      <div style={{ padding: "10px 16px", borderBottom: "1px solid var(--border-color)", backgroundColor: "var(--bg-secondary)", display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 13 }}>{surfaceIcon}<span style={{ color: surfaceColor, fontWeight: "bold" }}>{surfaceLabel}</span></div>
        <div style={{ flex: 1 }} />
        <button onClick={onFlipcardOpen} style={{ padding: "4px 10px", backgroundColor: "rgba(63,185,80,0.1)", border: "1px solid var(--accent-green)", color: "var(--accent-green)", borderRadius: 6, cursor: "pointer", fontSize: 12 }}>카드 학습</button>
        <button onClick={onClose} style={{ padding: "4px 10px", backgroundColor: "var(--bg-secondary)", border: "1px solid var(--border-color)", color: "var(--text-secondary)", borderRadius: 6, cursor: "pointer", fontSize: 12 }}>✕ 닫기</button>
      </div>
      <div style={{ flex: 1, overflowY: "auto" }}>
        {isLoading ? <div className="welcome-screen"><Loader className="spinner" /><p>로딩 중...</p></div> : <TermDetail term={term} siblingSenses={siblingSenses} englishMapping={englishMapping} onSenseSwitch={onSenseSwitch} onCrossLinkClick={onCrossLinkClick} onRelatedVocabClick={onRelatedVocabClick} showEnglish={showEnglish} />}
      </div>
    </div>
  );
}

function CoreListItem({ term, isSelected, onClick, showEnglish }) {
  return (
    <div onClick={onClick} style={{ padding: "10px 14px", marginBottom: 6, borderRadius: 8, cursor: "pointer", backgroundColor: isSelected ? "rgba(47,129,247,0.12)" : "var(--bg-secondary)", border: `1px solid ${isSelected ? "var(--accent-blue)" : "var(--border-color)"}`, display: "flex", alignItems: "center", gap: 10 }}>
      <span style={{ fontWeight: "bold", color: isSelected ? "var(--accent-blue)" : "var(--text-primary)" }}>{term.word}</span>
      {showEnglish && term.def_en && <span style={{ color: "var(--text-secondary)", fontSize: 13 }}>{term.def_en}</span>}
      {term.stats?.frequency_band && <span style={{ marginLeft: "auto", fontSize: 11, padding: "2px 7px", borderRadius: 10, backgroundColor: "rgba(88,166,255,0.12)", color: "var(--accent-blue)" }}>Band {term.stats.frequency_band}</span>}
    </div>
  );
}

export default App;
