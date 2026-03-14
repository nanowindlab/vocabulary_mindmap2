import React from "react";
import {
  Compass,
  Book,
  ExternalLink,
  Link as LinkIcon,
  AlertCircle,
} from "lucide-react";
import { localizeLabel } from "../utils/labelMap";
import "../index.css";

export const TermDetail = ({
  term,
  siblingSenses,
  englishMapping,
  onSenseSwitch,
  onCrossLinkClick,
  onRelatedVocabClick,
}) => {
  if (!term) return null;

  const {
    word,
    pos,
    def_ko,
    def_en,
    hierarchy,
    refs,
    stats,
    phonetic_romanization,
    qr_code_url,
    attested_sentences,
    related_vocab,
    examples_bundle,
    provenance,
    display_group,
  } = term;

  // ENGLISH MAPPING LOOKUP
  const getHelperEnglish = (korTerm) => {
    if (!englishMapping || !korTerm) return null;
    if (englishMapping.meta_groups?.[korTerm]?.en)
      return englishMapping.meta_groups[korTerm].en;
    if (englishMapping.example_styles?.[korTerm]?.en)
      return englishMapping.example_styles[korTerm].en;
    return null;
  };

  const getSafeExamples = () => {
    if (examples_bundle?.safe?.length > 0) return examples_bundle.safe;
    return (attested_sentences || []).filter(
      (ex) => ex.is_safe_example === true,
    );
  };

  const getStandardExamples = () => {
    if (examples_bundle?.standard?.length > 0) return examples_bundle.standard;
    return (attested_sentences || []).filter(
      (ex) => ex.is_safe_example !== true,
    );
  };

  const safeExamples = getSafeExamples();
  const standardExamples = getStandardExamples();

  return (
    <div className="detail-panel">
      {/* Surface Indicator */}
      <div style={{ marginBottom: 12 }}>
        <span
          className={`surface-badge ${
            term.surface === "mindmap_core"
              ? "core"
              : term.surface === "expression_core" || term.routing === "expression_core_candidate"
              ? "expr"
              : "meta"
          }`}
        >
          {term.surface === "mindmap_core"
            ? "코어 확장 맵"
            : term.surface === "expression_core" || term.routing === "expression_core_candidate"
            ? "표현 코어"
            : "메타 학습"}
        </span>
      </div>

      {/* Breadcrumb Path */}
      {hierarchy && hierarchy.path && (
        <div className="breadcrumb">
          {hierarchy.path.map((step, idx) => {
            const displayLabel = step.label || localizeLabel(step.id, step.id);
            return (
              <React.Fragment key={idx}>
                <span className="breadcrumb-item">{displayLabel}</span>
                {idx < hierarchy.path.length - 1 && (
                  <span style={{ opacity: 0.5, margin: "0 6px" }}>/</span>
                )}
              </React.Fragment>
            );
          })}
        </div>
      )}

      {/* Header */}
      <div className="term-header">
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
          }}
        >
          <div>
            <h2 className="term-word">{word}</h2>
            {term.routing !== "detail_only" && phonetic_romanization && (
              <div style={{ color: "var(--accent-purple)", marginBottom: 4 }}>
                /{phonetic_romanization}/
              </div>
            )}
            <span className="term-pos">{pos}</span>
            {display_group && (
              <span
                style={{
                  marginLeft: 8,
                  fontSize: 13,
                  color: "var(--text-secondary)",
                  backgroundColor: "var(--bg-secondary)",
                  padding: "2px 6px",
                  borderRadius: 4,
                }}
              >
                {display_group}{" "}
                {getHelperEnglish(display_group)
                  ? `(${getHelperEnglish(display_group)})`
                  : ""}
              </span>
            )}
          </div>
          {qr_code_url && (
            <a
              href={qr_code_url}
              target="_blank"
              rel="noreferrer"
              style={{
                padding: "8px",
                backgroundColor: "white",
                borderRadius: "8px",
              }}
            >
              <ExternalLink size={24} color="black" />
            </a>
          )}
        </div>
      </div>

      {/* Sense Switcher */}
      {siblingSenses && siblingSenses.length > 1 && (
        <div className="sense-switcher-container">
          <div className="section-subtitle">
            다른 뜻 보기 (다의망)
          </div>
          <div className="sense-chips">
            {(() => {
              const seen = new Set();
              const uniqueSenses = siblingSenses.filter((sense) => {
                if (sense.id === term.id) return true;
                // Normalize for stricter duplicate check
                const normalizedPos = (sense.pos || "").trim();
                const normalizedDef = (sense.def_ko || sense.def_en || sense.display_group || "")
                  .replace(/\s+/g, "")
                  .replace(/\.$/, "");
                const label = `${normalizedPos}_${normalizedDef}`;
                
                if (seen.has(label)) return false;
                seen.add(label);
                return true;
              });

              return uniqueSenses.map((sense) => (
                <button
                  key={sense.id}
                  onClick={() => onSenseSwitch && onSenseSwitch(sense)}
                  className={`sense-chip ${sense.id === term.id ? "active" : ""}`}
                >
                  {sense.pos && (
                    <span className="sense-pos-tag">
                      {sense.pos}
                    </span>
                  )}
                  <span className="sense-definition">
                    {sense.def_ko || sense.def_en || sense.display_group}
                  </span>
                  <span className="sense-surface-tag">
                    {sense.surface === "mindmap_core" ? "Core" : sense.surface === "expression_core" ? "Expr" : "Meta"}
                  </span>
                </button>
              ));
            })()}
          </div>
        </div>
      )}

      {/* Stats Block */}
      {stats && (
        <div className="stats-container">
          {stats.frequency_band && (
            <div className="stat-badge-band">
              <span className="label">Level</span>
              <span className="value">{stats.frequency_band}</span>
            </div>
          )}
          <div className="stat-group">
            {stats.total_frequency && (
              <span className="stat-item">빈도 <b>{stats.total_frequency.toLocaleString()}</b></span>
            )}
            {stats.source_count && (
              <span className="stat-item">출처 <b>{stats.source_count}</b></span>
            )}
            {stats.round_count && (
              <span className="stat-item">회차 <b>{stats.round_count}</b></span>
            )}
          </div>
        </div>
      )}

      {/* Top Sources Provenance (from chunk) */}
      {term.routing !== "detail_only" &&
        provenance &&
        provenance.top_sources &&
        provenance.top_sources.length > 0 && (
          <div style={{ marginTop: 24, marginBottom: 24 }}>
            <h3 className="section-title">
              <Compass size={18} /> 출처 요약 (Top Sources)
            </h3>
            <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
              {provenance.top_sources.map((src, idx) => (
                <span
                  key={idx}
                  style={{
                    padding: "2px 10px",
                    backgroundColor: "var(--bg-secondary)",
                    borderRadius: "16px",
                    fontSize: "13px",
                    color: "var(--text-primary)",
                    border: "1px solid var(--border-color)",
                  }}
                >
                  {src}
                </span>
              ))}
            </div>
          </div>
        )}

      {/* Definition Block */}
      <div className="def-container">
        <div className="def-en">{def_en}</div>
        <div className="def-ko">{def_ko}</div>
      </div>

      {/* Safe Examples (학습용 예문) */}
      {safeExamples.length > 0 ? (
        <div style={{ marginTop: 24 }}>
          <h3 className="section-title">
            <Book size={18} color="var(--accent-green)" /> 학습용 예문
          </h3>
          {safeExamples.map((ex, idx) => (
            <div
              key={`safe-${idx}`}
              className="example-card"
              style={{
                borderLeftColor: "var(--accent-green)",
                paddingBottom: 12,
              }}
            >
              <div className="ex-ko">{ex.ko}</div>
              <div className="ex-en" style={{ marginTop: 8 }}>
                {ex.en || ex.translation_en || ""}
              </div>
            </div>
          ))}
        </div>
      ) : term.routing !== "detail_only" ? (
        <div
          style={{
            marginTop: 24,
            padding: "12px",
            backgroundColor: "var(--bg-secondary)",
            borderRadius: "8px",
            fontStyle: "italic",
            color: "var(--text-secondary)",
            fontSize: "14px",
          }}
        >
          * 학습용 예문 준비 중
        </div>
      ) : null}

      {/* Standard Source Examples (실제 출처 예문) */}
      {standardExamples.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <h3 className="section-title">
            <Book size={18} color="var(--accent-purple)" /> 실제 출처 예문
            (TOPIK 등)
          </h3>
          <details
            style={{
              marginTop: "12px",
              padding: "8px",
              backgroundColor: "var(--bg-secondary)",
              borderRadius: "8px",
              border: "1px solid var(--border-color)",
            }}
          >
            <summary
              style={{
                cursor: "pointer",
                fontWeight: "bold",
                fontSize: "14px",
                color: "var(--text-primary)",
                outline: "none",
                padding: "4px",
              }}
            >
              관련 원문 출처 보기 ({standardExamples.length}개)
            </summary>
            <div style={{ marginTop: "12px" }}>
              {standardExamples.map((ex, idx) => (
                <div
                  key={`std-${idx}`}
                  className="example-card"
                  style={{
                    borderLeftColor: "var(--accent-purple)",
                    paddingBottom: 12,
                    marginBottom: 12,
                    backgroundColor: "transparent",
                  }}
                >
                  <div className="ex-ko">{ex.ko}</div>
                  {(ex.source_id || ex.round || ex.category) && (
                    <div className="ex-en" style={{ marginTop: 8 }}>
                      <span style={{ opacity: 0.7 }}>출처:</span>{" "}
                      {ex.source_id || "세종한국어 / TOPIK"}{" "}
                      {ex.round && `[${ex.round}]`}{" "}
                      {ex.category && `(${ex.category})`}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </details>
        </div>
      )}

      {/* Related Vocab Block */}
      {related_vocab && related_vocab.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <h3 className="section-title">
            <LinkIcon size={18} /> 연관 어휘
          </h3>
          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
            {related_vocab.map((rv, idx) => {
              const rvWord = typeof rv === "string" ? rv : rv.word;
              return (
                <span
                  key={idx}
                  onClick={() =>
                    onRelatedVocabClick && onRelatedVocabClick(rvWord)
                  }
                  style={{
                    padding: "4px 10px",
                    backgroundColor: "transparent",
                    borderRadius: "16px",
                    fontSize: "13px",
                    color: "var(--accent-blue)",
                    border: "1px solid var(--border-color)",
                    cursor: "pointer",
                  }}
                >
                  {rvWord}
                </span>
              );
            })}
          </div>
        </div>
      )}

      {/* Cross Links Block */}
      {refs && refs.cross_links && refs.cross_links.length > 0 && (
        <div style={{ marginTop: 40 }}>
          <h3
            className="section-title"
            style={{ color: "var(--accent-purple)" }}
          >
            <LinkIcon size={18} /> 확장 연결 경로 (Cross-Links)
          </h3>
          <div className="cross-links-grid">
            {refs.cross_links.map((link, idx) => (
              <div
                key={idx}
                className="cross-link-card"
                onClick={() => onCrossLinkClick(link)}
              >
                <div className="cross-link-target">
                  <span>연결 대상: {link.target_term || link.focus_term}</span>
                  <ExternalLink size={16} color="var(--accent-blue)" />
                </div>
                <div style={{ fontSize: 13, color: "#e6edf3", marginTop: 8 }}>
                  {[
                    link.target_center_id || link.center_id,
                    link.target_category_id || link.category_id,
                    link.target_subcenter_id || link.subcenter_id,
                  ]
                    .filter(Boolean)
                    .map((id) => localizeLabel(id))
                    .join(" ➔ ")}
                </div>
                <div className="cross-link-reason">
                  <AlertCircle
                    size={12}
                    style={{
                      display: "inline",
                      marginRight: 4,
                      verticalAlign: "middle",
                    }}
                  />
                  {link.reason}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
