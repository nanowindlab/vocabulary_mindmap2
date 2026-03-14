import React, { useState, useRef, useEffect } from "react";
import { Search } from "lucide-react";

export const SearchBox = ({
  searchIndex,
  onSelect,
  englishMapping,
  showEnglish,
}) => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const wrapperRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [wrapperRef]);

  const handleSearch = (e) => {
    const v = e.target.value;
    setQuery(v);
    if (!v.trim()) {
      setResults([]);
      setIsOpen(false);
      return;
    }

    // Simple filter
    const matches = searchIndex
      .filter(
        (item) =>
          item.word?.includes(v) ||
          item.def_ko?.includes(v) ||
          item.def_en?.toLowerCase().includes(v.toLowerCase()),
      )
      .slice(0, 10);

    setResults(matches);
    setIsOpen(true);
  };

  const handleItemClick = (item) => {
    onSelect(item);
    setIsOpen(false);
    setQuery("");
  };

  return (
    <div ref={wrapperRef} style={{ position: "relative", width: 260 }}>
      <div style={{ position: "relative" }}>
        <input
          type="text"
          placeholder="단어 검색..."
          value={query}
          onChange={handleSearch}
          onFocus={() => {
            if (query.trim()) setIsOpen(true);
          }}
          style={{
            width: "100%",
            padding: "6px 12px 6px 32px",
            borderRadius: 8,
            border: "1px solid var(--border-color)",
            backgroundColor: "rgba(22, 27, 34, 0.5)",
            color: "var(--text-primary)",
            fontSize: 13,
            outline: "none",
          }}
        />
        <Search
          size={14}
          color="var(--text-secondary)"
          style={{ position: "absolute", left: 10, top: 8 }}
        />
      </div>

      {isOpen && results.length > 0 && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            right: 0,
            marginTop: 4,
            backgroundColor: "var(--bg-tertiary)",
            border: "1px solid var(--border-color)",
            borderRadius: 8,
            overflow: "hidden",
            zIndex: 100,
            boxShadow: "0 8px 24px rgba(0,0,0,0.5)",
          }}
        >
          {results.map((res) => (
            <div
              key={res.id}
              onClick={() => handleItemClick(res)}
              style={{
                padding: "8px 12px",
                cursor: "pointer",
                borderBottom: "1px solid rgba(255,255,255,0.05)",
                display: "flex",
                flexDirection: "column",
                gap: 4,
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.backgroundColor = "var(--bg-secondary)")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.backgroundColor = "transparent")
              }
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <span
                  style={{
                    fontWeight: 600,
                    fontSize: 13,
                    color: "var(--text-primary)",
                  }}
                >
                  {res.word}
                </span>
                <span
                  style={{
                    fontSize: 11,
                    color: "var(--text-secondary)",
                    padding: "2px 6px",
                    borderRadius: 4,
                    backgroundColor: "rgba(255,255,255,0.05)",
                  }}
                >
                  {res.routing === "meta_learning"
                    ? "메타"
                    : res.routing === "expression_core"
                      ? "표현"
                      : "코어"}
                </span>
              </div>
              <div
                style={{
                  fontSize: 12,
                  color: "var(--text-secondary)",
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                }}
              >
                {res.def_ko} {showEnglish && res.def_en && ` - ${res.def_en}`}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
