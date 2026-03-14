import React, { useState } from "react";
import {
  BookOpen,
  Hash,
  Link as LinkIcon,
  Volume2,
  Languages,
  Share2,
  Globe,
} from "lucide-react";

// ── V3 명세 방어 함수 ────────────────────────────────────────────
const safeBand = (stats) => {
  if (!stats) return null;
  const b = stats.band;
  if (b === null || b === undefined) return null;
  return typeof b === "number" && b >= 1 && b <= 5 ? b : null;
};

// V8 명세 국문 Band 명칭
const BAND_META = {
  1: { label: "최상위 필수",  label_en: "Essential", color: "#ff7b72", bg: "rgba(255,123,114,0.15)", border: "rgba(255,123,114,0.4)" },
  2: { label: "핵심 중요",    label_en: "High",       color: "#ffa657", bg: "rgba(255,166,87,0.15)",  border: "rgba(255,166,87,0.4)"  },
  3: { label: "일반 활용",    label_en: "Medium",     color: "#e3b341", bg: "rgba(227,179,65,0.15)",  border: "rgba(227,179,65,0.4)"  },
  4: { label: "보조 표현",    label_en: "Low",        color: "#3fb950", bg: "rgba(63,185,80,0.15)",   border: "rgba(63,185,80,0.4)"   },
  5: { label: "심화 어휘",    label_en: "Rare",       color: "#58a6ff", bg: "rgba(88,166,255,0.15)",  border: "rgba(88,166,255,0.4)"  },
};

const LEVEL_META = {
  Beginner:     { label: "초급 (Beginner)",    color: "#79c0ff" },
  Intermediate: { label: "중급 (Intermediate)", color: "#d2a8ff" },
  Advanced:     { label: "고급 (Advanced)",     color: "#ffa657" },
  Unrated:      { label: "레벨 미산출",          color: "#6e7681" },
};

const safeLevel = (stats) => {
  if (!stats) return "Unrated";
  return stats.level || "Unrated";
};

// ── 컴포넌트 ─────────────────────────────────────────────────────
export const TermDetail = ({
  term,
  siblingSenses = [],
  englishMapping,
  onSenseSwitch,
  onCrossLinkClick,
  onRelatedVocabClick,
  showEnglish,
}) => {
  if (!term) return null;

  const [activeTab, setActiveTab] = useState("def");
  const isVirtual = term.routing === "detail_only";

  const band = safeBand(term.stats);
  const level = safeLevel(term.stats);
  const bandMeta = band ? BAND_META[band] : null;
  const levelMeta = LEVEL_META[level] || LEVEL_META.Unrated;
  const roman = term.phonetic_romanization || term.roman || "";
  const defKo = term.def_ko || term.def_kr || "";
  const defEn = term.def_en || "";
  const pos = term.pos || term.part_of_speech || "";

  const renderRelatedChips = (items, onClick) => {
    if (!items || items.length === 0) return null;
    return (
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 10 }}>
        {items.map((i, idx) => {
          const word = typeof i === "string" ? i : i.label || i;
          const clickable = !!onClick;
          return (
            <span
              key={idx}
              onClick={() => clickable && onClick(word)}
              title={clickable ? `'${word}' 탐색` : word}
              style={{
                padding: "5px 12px",
                borderRadius: 16,
                background: clickable
                  ? "linear-gradient(135deg, rgba(88,166,255,0.1), rgba(188,140,255,0.1))"
                  : "rgba(255,255,255,0.05)",
                border: clickable
                  ? "1px solid rgba(88,166,255,0.35)"
                  : "1px solid var(--border-color)",
                fontSize: 13,
                fontWeight: 500,
                color: clickable ? "var(--accent-blue)" : "var(--text-secondary)",
                cursor: clickable ? "pointer" : "default",
                transition: "all 0.18s",
                userSelect: "none",
              }}
              onMouseEnter={(e) => {
                if (clickable) {
                  e.currentTarget.style.background = "linear-gradient(135deg, rgba(88,166,255,0.22), rgba(188,140,255,0.22))";
                  e.currentTarget.style.borderColor = "rgba(88,166,255,0.7)";
                  e.currentTarget.style.transform = "translateY(-1px)";
                  e.currentTarget.style.boxShadow = "0 3px 10px rgba(88,166,255,0.25)";
                }
              }}
              onMouseLeave={(e) => {
                if (clickable) {
                  e.currentTarget.style.background = "linear-gradient(135deg, rgba(88,166,255,0.1), rgba(188,140,255,0.1))";
                  e.currentTarget.style.borderColor = "rgba(88,166,255,0.35)";
                  e.currentTarget.style.transform = "none";
                  e.currentTarget.style.boxShadow = "none";
                }
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    );
  };

  const renderChips = (items, onClick) => {
    if (!items || items.length === 0) return null;
    return (
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 8 }}>
        {items.map((i, idx) => (
          <span
            key={idx}
            onClick={() => onClick && onClick(i)}
            style={{
              padding: "4px 10px", borderRadius: 12,
              backgroundColor: "rgba(255,255,255,0.05)",
              border: "1px solid var(--border-color)",
              fontSize: 12, color: "var(--text-secondary)",
              cursor: onClick ? "pointer" : "default",
              transition: "all 0.15s",
            }}
            onMouseEnter={(e) => {
              if (onClick) {
                e.currentTarget.style.backgroundColor = "var(--bg-tertiary)";
                e.currentTarget.style.color = "var(--text-primary)";
              }
            }}
            onMouseLeave={(e) => {
              if (onClick) {
                e.currentTarget.style.backgroundColor = "rgba(255,255,255,0.05)";
                e.currentTarget.style.color = "var(--text-secondary)";
              }
            }}
          >
            {typeof i === "string" ? i : i.label || i}
          </span>
        ))}
      </div>
    );
  };


  return (
    <div style={{ flex: 1, display: "flex", flexDirection: "column", height: "100%", backgroundColor: "var(--bg-primary)" }}>

      {/* ── 헤더 ── */}
      <div style={{ padding: "24px 24px 16px", borderBottom: "1px solid var(--border-color)", backgroundColor: "rgba(22,27,34,0.5)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
          {/* 단어 + 발음 */}
          <div>
            <div style={{ fontSize: 32, fontWeight: 700, color: "var(--text-primary)", letterSpacing: "-0.5px" }}>
              {term.word}
            </div>
            {roman && (
              <div style={{ display: "flex", alignItems: "center", gap: 6, color: "var(--accent-purple)", marginTop: 6, fontSize: 14 }}>
                <Volume2 size={14} /> <span>[{roman}]</span>
              </div>
            )}
          </div>

          {/* Band + Level 배지 (우측 상단) */}
          <div style={{ display: "flex", flexDirection: "column", gap: 6, alignItems: "flex-end" }}>
            {bandMeta ? (
              <span style={{
                padding: "5px 12px", borderRadius: 8, fontSize: 13, fontWeight: 700,
                color: bandMeta.color, background: bandMeta.bg, border: `1.5px solid ${bandMeta.border}`,
                whiteSpace: "nowrap",
              }}>
                Band {band} · {bandMeta.label}
              </span>
            ) : (
              <span style={{
                padding: "5px 12px", borderRadius: 8, fontSize: 12, fontWeight: 500,
                color: "#6e7681", background: "rgba(110,118,129,0.08)", border: "1px solid rgba(110,118,129,0.2)",
              }}>Band 미산출</span>
            )}
            <span style={{
              padding: "3px 10px", borderRadius: 6, fontSize: 12, fontWeight: 500,
              color: levelMeta.color, background: levelMeta.color + "20", border: `1px solid ${levelMeta.color}40`,
            }}>
              {levelMeta.label}
            </span>
          </div>
        </div>

        {/* 메타 태그 — 빈도수 숫자 제거, path_ko만 노출 */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 12 }}>
          {pos && (
            <span style={{ fontSize: 12, color: "var(--text-secondary)", border: "1px solid var(--border-color)", padding: "2px 8px", borderRadius: 12 }}>
              {pos}
            </span>
          )}
          {term.hierarchy?.path_ko && (
            <span style={{ fontSize: 12, color: "var(--text-secondary)", border: "1px solid var(--border-color)", padding: "2px 8px", borderRadius: 12 }}>
              {term.hierarchy.path_ko}
            </span>
          )}
        </div>
      </div>

      {/* ── 탭 (통계 탭 제거) ── */}
      <div style={{ display: "flex", borderBottom: "1px solid var(--border-color)", padding: "0 16px" }}>
        {[
          { key: "def",      label: "정의 & 연관" },
          { key: "examples", label: "예문" },
        ].map((t) => (
          <button
            key={t.key}
            onClick={() => setActiveTab(t.key)}
            style={{
              ...tabBtnStyle,
              color: activeTab === t.key ? "var(--accent-blue)" : "var(--text-secondary)",
              borderBottomColor: activeTab === t.key ? "var(--accent-blue)" : "transparent",
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* ── 콘텐츠 ── */}
      <div style={{ flex: 1, overflowY: "auto", padding: "24px" }}>

        {/* 정의 탭 */}
        {activeTab === "def" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
            {!isVirtual && (
              <div className="card-glass" style={{ padding: 20, borderRadius: 12 }}>
                <div style={{ fontSize: 16, fontWeight: 500, color: "var(--text-primary)", lineHeight: 1.6 }}>
                  {defKo || "정의 없음"}
                </div>
                {showEnglish && defEn && (
                  <div style={{ fontSize: 14, color: "var(--text-secondary)", marginTop: 10, borderTop: "1px solid rgba(255,255,255,0.08)", paddingTop: 10, display: "flex", alignItems: "flex-start", gap: 6 }}>
                    <Globe size={14} style={{ marginTop: 2, flexShrink: 0, opacity: 0.7 }} />
                    <span style={{ fontStyle: "italic" }}>{defEn}</span>
                  </div>
                )}
              </div>
            )}
            {isVirtual && (
              <div style={{ color: "var(--text-secondary)", fontStyle: "italic", padding: "20px 0" }}>
                (관련 어휘로 탐색 중 — 코어 상세 정보가 없습니다)
              </div>
            )}

            {/* 연관 어휘 */}
            {term.related_vocab && term.related_vocab.length > 0 && (
              <div>
                <h4 style={{ display: "flex", alignItems: "center", gap: 6, color: "var(--text-secondary)", fontSize: 12, marginBottom: 8, textTransform: "uppercase", letterSpacing: 1 }}>
                  <Share2 size={13} /> 연관 어휘
                </h4>
                {renderRelatedChips(term.related_vocab, onRelatedVocabClick)}
              </div>
            )}

            {/* 교차 연결 */}
            {term.refs?.cross_links && term.refs.cross_links.length > 0 && (
              <div>
                <h4 style={{ display: "flex", alignItems: "center", gap: 6, color: "var(--accent-blue)", fontSize: 12, marginBottom: 8, textTransform: "uppercase", letterSpacing: 1 }}>
                  <LinkIcon size={13} /> 교차 연결 장면
                </h4>
                {renderChips(
                  term.refs.cross_links.map((c) => ({ label: `${c.target_term} ➔ ${c.target_category || c.target_center_id || ""}`, value: c })),
                  (val) => onCrossLinkClick && onCrossLinkClick(val.value),
                )}
              </div>
            )}

            {/* 동음이의어 */}
            {siblingSenses.length > 1 && (
              <div>
                <h4 style={{ display: "flex", alignItems: "center", gap: 6, color: "var(--accent-orange)", fontSize: 12, marginBottom: 8, textTransform: "uppercase", letterSpacing: 1 }}>
                  <Hash size={13} /> 다른 뜻 보기
                </h4>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                  {siblingSenses.filter((s) => s.id !== term.id).map((sib) => (
                    <button key={sib.id} onClick={() => onSenseSwitch(sib)}
                      style={{ padding: "8px 12px", backgroundColor: "var(--bg-secondary)", border: "1px solid var(--border-color)", borderRadius: 8, color: "var(--text-primary)", cursor: "pointer", fontSize: 13, textAlign: "left" }}>
                      <div style={{ fontWeight: 600, color: "var(--accent-orange)" }}>{sib.word}</div>
                      <div style={{ fontSize: 12, color: "var(--text-secondary)", marginTop: 4 }}>
                        {showEnglish && sib.def_en ? sib.def_en : sib.def_ko}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* 예문 탭 */}
        {activeTab === "examples" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {!term.examples_bundle || term.examples_bundle.length === 0 ? (
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "40px 0", color: "var(--text-secondary)" }}>
                <BookOpen size={24} style={{ marginBottom: 12, opacity: 0.5 }} />
                <span>예문 데이터가 없습니다.</span>
              </div>
            ) : (
              term.examples_bundle.map((ex, idx) => (
                <div key={idx} className="card-glass" style={{ padding: "16px 20px", borderRadius: 12, borderLeft: "3px solid var(--accent-blue)" }}>
                  <div style={{ fontSize: 15, color: "var(--text-primary)", lineHeight: 1.6, marginBottom: 8 }}>
                    {ex.text_ko}
                  </div>
                  {showEnglish && ex.text_en && (
                    <div style={{ display: "flex", alignItems: "flex-start", gap: 6, fontSize: 13, color: "var(--text-secondary)", fontStyle: "italic", borderTop: "1px solid var(--border-color)", paddingTop: 8 }}>
                      <Globe size={12} style={{ marginTop: 2, flexShrink: 0, opacity: 0.7 }} />
                      {ex.text_en}
                    </div>
                  )}
                  {ex.source && (
                    <div style={{ marginTop: 8, fontSize: 11, color: "var(--text-secondary)", opacity: 0.5, textAlign: "right", letterSpacing: 0.5 }}>
                      {ex.source}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};

const tabBtnStyle = {
  all: "unset", padding: "12px 20px", fontSize: 14, fontWeight: 600,
  cursor: "pointer", borderBottom: "2px solid transparent",
  transition: "all 0.2s ease", flex: 1, textAlign: "center",
};
