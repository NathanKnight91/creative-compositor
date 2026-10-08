import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { Card, Mono, SceneShell, useEntrance } from "../components";
import { colors } from "../theme";

type Node = { id: string; label: string; sub: string; x: number; y: number; w: number; delay: number; core?: boolean };

const NODES: Node[] = [
  { id: "app", label: "app.py", sub: "Router · picks a tool from the sidebar", x: 660, y: 270, w: 600, delay: 5 },
  { id: "overlay", label: "tools/overlay_tool.py", sub: "Position · preview · batch render", x: 300, y: 470, w: 560, delay: 25 },
  { id: "text", label: "tools/text_tool.py", sub: "3-line text design", x: 1060, y: 470, w: 560, delay: 35 },
  { id: "ui", label: "ui/", sub: "styles · preview", x: 120, y: 690, w: 420, delay: 55 },
  { id: "utils", label: "utils/", sub: "file_scanner", x: 1380, y: 690, w: 420, delay: 60 },
  { id: "core", label: "compositor.py", sub: "Pillow + FFmpeg engine · config.json", x: 660, y: 690, w: 600, delay: 75, core: true },
];

const EDGES: [string, string][] = [
  ["app", "overlay"],
  ["app", "text"],
  ["overlay", "core"],
  ["text", "core"],
  ["overlay", "ui"],
  ["text", "utils"],
];

const H = 120;
const center = (n: Node) => ({ x: n.x + n.w / 2, y: n.y + H / 2 });

export const Architecture: React.FC = () => {
  const frame = useCurrentFrame();
  const byId = Object.fromEntries(NODES.map((n) => [n.id, n]));
  const note = useEntrance(110);

  return (
    <SceneShell kicker="Under the hood" title="Modular by design">
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        {EDGES.map(([a, b], i) => {
          const p = center(byId[a]);
          const q = center(byId[b]);
          const len = Math.hypot(q.x - p.x, q.y - p.y);
          const draw = interpolate(frame, [40 + i * 6, 70 + i * 6], [len, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          return (
            <line
              key={`${a}-${b}`}
              x1={p.x}
              y1={p.y}
              x2={q.x}
              y2={q.y}
              stroke={colors.accent}
              strokeOpacity={0.6}
              strokeWidth={3}
              strokeDasharray={len}
              strokeDashoffset={draw}
            />
          );
        })}
      </svg>
      {NODES.map((n) => {
        const s = useEntrance(n.delay);
        return (
          <Card
            key={n.id}
            style={{
              position: "absolute",
              left: n.x,
              top: n.y,
              width: n.w,
              height: H,
              boxSizing: "border-box",
              padding: "20px 28px",
              opacity: s,
              transform: `scale(${0.85 + 0.15 * s})`,
              border: `2px solid ${n.core ? colors.accent : colors.border}`,
              background: n.core ? colors.bgElevated : colors.bgCard,
            }}
          >
            <Mono style={{ fontSize: 30, fontWeight: 700, color: n.core ? colors.accent : colors.textPrimary }}>
              {n.label}
            </Mono>
            <div style={{ fontSize: 22, color: colors.textMuted, marginTop: 8 }}>{n.sub}</div>
          </Card>
        );
      })}
      <div
        style={{
          position: "absolute",
          top: 880,
          left: 0,
          right: 0,
          textAlign: "center",
          fontSize: 30,
          color: colors.textMuted,
          opacity: note,
        }}
      >
        New tool? Add <Mono style={{ color: colors.textPrimary }}>tools/your_tool.py</Mono> with a{" "}
        <Mono style={{ color: colors.accent }}>render(comp, inputs, base_path)</Mono> and register it in{" "}
        <Mono style={{ color: colors.textPrimary }}>app.py</Mono>.
      </div>
    </SceneShell>
  );
};
