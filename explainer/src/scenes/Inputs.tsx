import React from "react";
import { Card, Mono, SceneShell, useEntrance } from "../components";
import { colors } from "../theme";

const TREE: { depth: number; name: string; note?: string }[] = [
  { depth: 0, name: "inputs/" },
  { depth: 1, name: "heroes/" },
  { depth: 2, name: "1x1/", note: "PNG · JPG" },
  { depth: 2, name: "9x16/", note: "PNG · JPG" },
  { depth: 1, name: "overlays/" },
  { depth: 2, name: "static/1x1/  static/9x16/", note: "transparent PNG" },
  { depth: 2, name: "video/1x1/   video/9x16/", note: "MOV / MP4 with alpha" },
];

export const Inputs: React.FC = () => {
  const side = useEntrance(80);
  return (
    <SceneShell kicker="Step 1" title="Drop assets into folders">
      <Card style={{ position: "absolute", top: 290, left: 120, width: 1020, padding: "40px 50px" }}>
        {TREE.map((row, i) => {
          const s = useEntrance(10 + i * 8);
          return (
            <div
              key={row.name}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                fontSize: 32,
                padding: "10px 0",
                paddingLeft: row.depth * 56,
                opacity: s,
                transform: `translateX(${(1 - s) * -40}px)`,
              }}
            >
              <Mono style={{ color: row.depth === 0 ? colors.accent : colors.textPrimary }}>
                {row.name}
              </Mono>
              {row.note ? (
                <span style={{ fontSize: 24, color: colors.textMuted }}>{row.note}</span>
              ) : null}
            </div>
          );
        })}
      </Card>
      <div
        style={{
          position: "absolute",
          top: 330,
          left: 1220,
          width: 580,
          fontSize: 32,
          lineHeight: 1.5,
          color: colors.textMuted,
          opacity: side,
          transform: `translateY(${(1 - side) * 30}px)`,
        }}
      >
        <Mono style={{ color: colors.textPrimary }}>utils/file_scanner.py</Mono> walks
        each folder, groups files by{" "}
        <span style={{ color: colors.accent }}>campaign subfolder</span>, and
        pairs every hero only with overlays of the{" "}
        <span style={{ color: colors.accent }}>same aspect ratio</span>.
      </div>
    </SceneShell>
  );
};
