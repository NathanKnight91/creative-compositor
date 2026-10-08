import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { Card, HeroArt, SceneShell, useEntrance } from "../components";
import { colors } from "../theme";

const LINES = [
  { text: "THE NEW SERIES", size: 34, weight: 400, italic: false, style: "Regular · 34px" },
  { text: "Starts Tonight", size: 64, weight: 900, italic: false, style: "Bold · 64px" },
  { text: "only on streaming", size: 30, weight: 400, italic: true, style: "Italic · 30px" },
];

export const TextTool: React.FC = () => {
  const frame = useCurrentFrame();
  const panel = useEntrance(5);
  const align = frame < 120 ? "left" : "center";
  const alignLabel = frame < 120 ? "Left" : "Center";

  return (
    <SceneShell kicker="Tool 2" title="3-line text overlays">
      <Card
        style={{
          position: "absolute",
          top: 290,
          left: 120,
          width: 760,
          padding: "34px 40px",
          opacity: panel,
        }}
      >
        {LINES.map((line, i) => {
          const s = useEntrance(15 + i * 15);
          const typed = Math.round(
            interpolate(frame, [15 + i * 15, 45 + i * 15], [0, line.text.length], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            })
          );
          return (
            <div key={i} style={{ marginBottom: 26, opacity: s }}>
              <div style={{ fontSize: 20, color: colors.textMuted, marginBottom: 8 }}>
                Line {i + 1} · {line.style}
              </div>
              <div
                style={{
                  fontSize: 28,
                  padding: "12px 18px",
                  borderRadius: 8,
                  background: colors.bgElevated,
                  border: `1px solid ${colors.border}`,
                }}
              >
                {line.text.slice(0, typed)}
                <span style={{ color: colors.accent }}>{typed < line.text.length ? "|" : ""}</span>
              </div>
            </div>
          );
        })}
        <div style={{ display: "flex", gap: 14, fontSize: 22, marginTop: 6 }}>
          {["Left", "Center", "Right"].map((a) => (
            <div
              key={a}
              style={{
                padding: "10px 22px",
                borderRadius: 8,
                border: `1px solid ${a === alignLabel ? colors.accent : colors.border}`,
                color: a === alignLabel ? colors.accent : colors.textMuted,
              }}
            >
              {a}
            </div>
          ))}
          <div style={{ marginLeft: "auto", color: colors.textMuted, alignSelf: "center" }}>
            Font family · Colour · Line spacing
          </div>
        </div>
      </Card>

      <div style={{ position: "absolute", top: 260, left: 1040, opacity: panel }}>
        <HeroArt width={420} height={746} hue={300}>
          <div
            style={{
              position: "absolute",
              left: 36,
              right: 36,
              bottom: 120,
              textAlign: align,
              fontFamily: "Arial, sans-serif",
              color: "#fff",
              textShadow: "0 4px 20px rgba(0,0,0,0.5)",
            }}
          >
            {LINES.map((line, i) => (
              <div
                key={i}
                style={{
                  fontSize: line.size * 0.62,
                  fontWeight: line.weight,
                  fontStyle: line.italic ? "italic" : "normal",
                  lineHeight: 1.25,
                  opacity: useEntrance(30 + i * 15),
                }}
              >
                {line.text}
              </div>
            ))}
          </div>
        </HeroArt>
        <div style={{ textAlign: "center", fontSize: 22, color: colors.textMuted, marginTop: 14 }}>
          9x16 preview
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          top: 420,
          left: 1520,
          width: 300,
          fontSize: 28,
          lineHeight: 1.5,
          color: colors.textMuted,
          opacity: useEntrance(90),
        }}
      >
        Each line gets its own <span style={{ color: colors.accent }}>font style and size</span>, rendered
        with Pillow from <span style={{ color: colors.textPrimary }}>assets/fonts/</span>.
      </div>
    </SceneShell>
  );
};
