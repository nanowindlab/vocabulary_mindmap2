import React, { useRef, useEffect, useState, useCallback } from "react";
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
import {
  Network,
  Map,
  Layers,
  Target,
  BookOpen,
  ZoomIn,
  ZoomOut,
  RefreshCcw,
  Link as LinkIcon,
} from "lucide-react";

// ── 노드 타입별 스타일 설정 ─────────────────────────────────────────────────────
const NODE_STYLE = {
  root: {
    bg: "rgba(88,166,255,0.18)",
    border: "#58a6ff",
    color: "#58a6ff",
    radius: 26,
    fontSize: 15,
    fontWeight: "bold",
  },
  scene: {
    bg: "rgba(63,185,80,0.15)",
    border: "#3fb950",
    color: "#3fb950",
    radius: 22,
    fontSize: 14,
    fontWeight: "bold",
  },
  center: {
    bg: "rgba(63,185,80,0.15)",
    border: "#3fb950",
    color: "#3fb950",
    radius: 22,
    fontSize: 14,
    fontWeight: "bold",
  },
  category: {
    bg: "rgba(188,140,255,0.12)",
    border: "#bc8cff",
    color: "#bc8cff",
    radius: 8,
    fontSize: 13,
    fontWeight: "600",
  },
  subcenter: {
    bg: "rgba(255,166,87,0.12)",
    border: "#ffa657",
    color: "#ffa657",
    radius: 8,
    fontSize: 12,
    fontWeight: "normal",
  },
  term: {
    bg: "rgba(139,148,158,0.10)",
    border: "#444c56",
    color: "#cdd9e5",
    radius: 20,
    fontSize: 13,
    fontWeight: "normal",
  },
};

// ── SVG 연결선 ──────────────────────────────────────────────────────────────────
const Connector = ({ x1, y1, x2, y2, color = "rgba(100,120,150,0.35)" }) => (
  <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={1.5} />
);

// ── 개별 노드 (absolute 배치) ───────────────────────────────────────────────────
const MindNode = ({ node, x, y, isSelected, onClick, onLinkClick }) => {
  const style = NODE_STYLE[node.type] || NODE_STYLE.term;
  const padH = node.type === "root" ? 22 : node.type === "term" ? 14 : 12;
  const padV = node.type === "root" ? 14 : 8;
  const hasLinks = node.data?.refs?.cross_links?.length > 0;

  return (
    <div
      onClick={() => onClick && onClick(node)}
      className="mind-node"
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: "translate(-50%, -50%)",
        padding: `${padV}px ${padH}px`,
        background: isSelected ? "rgba(47,129,247,0.25)" : style.bg,
        border: `1.5px solid ${isSelected ? "var(--accent-blue)" : style.border}`,
        borderRadius: style.radius,
        color: isSelected ? "var(--accent-blue)" : style.color,
        fontSize: style.fontSize,
        fontWeight: style.fontWeight,
        whiteSpace: "nowrap",
        cursor: node.type === "term" ? "pointer" : "default",
        boxShadow: isSelected
          ? "0 0 0 3px rgba(47,129,247,0.35)"
          : node.type === "root"
            ? "0 4px 18px rgba(0,0,0,0.35)"
            : "0 1px 6px rgba(0,0,0,0.2)",
        transition: "all 0.2s",
        zIndex: node.type === "root" ? 10 : node.type === "scene" ? 8 : 5,
        userSelect: "none",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
        {node.label}
        {hasLinks && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              if (onLinkClick) onLinkClick(node.data.refs.cross_links[0]);
            }}
            style={{
              all: "unset",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: "2px",
              borderRadius: "4px",
              backgroundColor: "rgba(88,166,255,0.15)",
              transition: "transform 0.1s ease-in-out",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.2)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1.0)")}
            title="다른 관련 장면으로 이동"
          >
            <LinkIcon size={12} color="var(--accent-blue)" />
          </button>
        )}
      </div>
    </div>
  );
};

// ── 방사형 계산 헬퍼 ────────────────────────────────────────────────────────────
const polar = (cx, cy, r, angleDeg) => ({
  x: cx + r * Math.cos((angleDeg * Math.PI) / 180),
  y: cy + r * Math.sin((angleDeg * Math.PI) / 180),
});

// ── 단일 대분류 방사형 렌더러 ──────────────────────────────────────────────────
const renderRadialTree = (
  rootNode,
  cx,
  cy,
  selectedTermId,
  onSelectTerm,
  nodes,
  lines,
) => {
  // 루트 노드
  nodes.push({
    node: rootNode,
    x: cx,
    y: cy,
    isSelected: selectedTermId === rootNode.id,
  });

  const scenes = Object.values(rootNode.children || {});
  const sceneCount = scenes.length;
  if (sceneCount === 0) return;

  const outerR = 220; // 중심에서 scene 까지의 거리
  const SCENE_ANGLES =
    sceneCount === 1 ? [0] : scenes.map((_, i) => (360 / sceneCount) * i - 90);

  scenes.forEach((scene, si) => {
    const angleRad = (SCENE_ANGLES[si] * Math.PI) / 180;
    const sx = cx + outerR * Math.cos(angleRad);
    const sy = cy + outerR * Math.sin(angleRad);

    nodes.push({
      node: scene,
      x: sx,
      y: sy,
      isSelected: selectedTermId === scene.id,
    });
    lines.push({ x1: cx, y1: cy, x2: sx, y2: sy });

    const categories = Object.values(scene.children || {});
    const catCount = categories.length;
    if (catCount === 0) return;

    // 각 scene 아래의 카테고리들: scene 기준으로 ±60° 부채꼴 퍼트리기
    const catSpread = 60;
    const catRadius = 140;
    const catAngles =
      catCount === 1
        ? [SCENE_ANGLES[si]]
        : categories.map(
            (_, ci) =>
              SCENE_ANGLES[si] -
              catSpread / 2 +
              (catSpread / (catCount - 1)) * ci,
          );

    categories.forEach((cat, ci) => {
      const caRad = (catAngles[ci] * Math.PI) / 180;
      const cx2 = sx + catRadius * Math.cos(caRad);
      const cy2 = sy + catRadius * Math.sin(caRad);

      nodes.push({
        node: cat,
        x: cx2,
        y: cy2,
        isSelected: selectedTermId === cat.id,
      });
      lines.push({ x1: sx, y1: sy, x2: cx2, y2: cy2 });

      const terms = Object.values(cat.children || {});
      const termCount = terms.length;
      if (termCount === 0) return;

      const termSpread = Math.min(50, termCount * 12);
      const termRadius = 100;
      const termAngles =
        termCount === 1
          ? [catAngles[ci]]
          : terms.map(
              (_, ti) =>
                catAngles[ci] -
                termSpread / 2 +
                (termSpread / (termCount - 1)) * ti,
            );

      terms.forEach((term, ti) => {
        const trRad = (termAngles[ti] * Math.PI) / 180;
        const tx = cx2 + termRadius * Math.cos(trRad);
        const ty = cy2 + termRadius * Math.sin(trRad);

        nodes.push({
          node: term,
          x: tx,
          y: ty,
          isSelected:
            selectedTermId === term.id || selectedTermId === term.data?.id,
        });
        lines.push({ x1: cx2, y1: cy2, x2: tx, y2: ty });
      });
    });
  });
};

// ── 메인 컴포넌트 ───────────────────────────────────────────────────────────────
export const MindmapCanvas = ({
  treeData,
  onSelectTerm,
  onCrossLinkClick,
  selectedTermId,
  focusedRootId,
}) => {
  const CANVAS_W = 2400;
  const CANVAS_H = 2400;

  // 렌더링할 루트 결정: focusedRootId가 있으면 해당 루트만
  const rootsToRender = focusedRootId
    ? Object.values(treeData).filter((r) => r.id === focusedRootId)
    : Object.values(treeData);

  // 각 root를 격자 배치 (최대 3열)
  const cols = Math.min(3, rootsToRender.length);
  const cellW = CANVAS_W / cols;
  const cellH = CANVAS_H / Math.ceil(rootsToRender.length / cols);

  const allNodes = [];
  const allLines = [];

  rootsToRender.forEach((rootNode, idx) => {
    const col = idx % cols;
    const row = Math.floor(idx / cols);
    const cx = cellW * col + cellW / 2;
    const cy = cellH * row + cellH / 2;
    renderRadialTree(
      rootNode,
      cx,
      cy,
      selectedTermId,
      onSelectTerm,
      allNodes,
      allLines,
    );
  });

  const handleNodeClick = (node) => {
    if (node.type === "term" && node.data) {
      onSelectTerm(node.data);
    }
  };

  const handleLinkClick = (link) => {
    if (onCrossLinkClick) {
      onCrossLinkClick(link);
    }
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        overflow: "hidden",
        backgroundColor: "#0d1117",
        position: "relative",
      }}
    >
      <TransformWrapper
        initialScale={0.45}
        minScale={0.1}
        maxScale={3}
        centerOnInit={true}
        wheel={{ step: 0.08 }}
        limitToBounds={false}
      >
        {({ zoomIn, zoomOut, resetTransform }) => (
          <>
            {/* 줌 컨트롤 */}
            <div
              style={{
                position: "absolute",
                top: 12,
                right: 12,
                zIndex: 20,
                display: "flex",
                flexDirection: "column",
                gap: 6,
              }}
            >
              {[
                { icon: <ZoomIn size={14} />, action: () => zoomIn() },
                { icon: <ZoomOut size={14} />, action: () => zoomOut() },
                {
                  icon: <RefreshCcw size={14} />,
                  action: () => resetTransform(),
                },
              ].map((btn, i) => (
                <button
                  key={i}
                  onClick={btn.action}
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: 6,
                    border: "1px solid rgba(255,255,255,0.1)",
                    backgroundColor: "rgba(22,27,34,0.9)",
                    color: "#cdd9e5",
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  {btn.icon}
                </button>
              ))}
            </div>

            <TransformComponent
              wrapperStyle={{ width: "100%", height: "100%" }}
            >
              <div
                style={{
                  position: "relative",
                  width: CANVAS_W,
                  height: CANVAS_H,
                }}
              >
                {/* SVG 연결선 */}
                <svg
                  style={{
                    position: "absolute",
                    top: 0,
                    left: 0,
                    width: CANVAS_W,
                    height: CANVAS_H,
                    pointerEvents: "none",
                    zIndex: 1,
                  }}
                >
                  {allLines.map((line, i) => (
                    <Connector key={i} {...line} />
                  ))}
                </svg>

                {/* 노드들 */}
                {allNodes.map((n, i) => (
                  <MindNode
                    key={n.node.id + "-" + i}
                    node={n.node}
                    x={n.x}
                    y={n.y}
                    isSelected={n.isSelected}
                    onClick={handleNodeClick}
                    onLinkClick={handleLinkClick}
                  />
                ))}
              </div>
            </TransformComponent>
          </>
        )}
      </TransformWrapper>
    </div>
  );
};
