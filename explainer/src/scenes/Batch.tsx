import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { Card, HeroArt, Mono, OverlayBadge, SceneShell, useEntrance } from "../components";
import { colors } from "../theme";

const OUTPUTS = [
  "outputs/1x1/v2/hero_a_logo.png",
  "outputs/1x1/v2/hero_a_sting.mp4",
  "outputs/1x1/v2/hero_b_logo.png",
  "outputs/1x1/v2/hero_b_sting.mp4",
  "outputs/9x16/v2/hero_c_logo.png",
  "outputs/9x16/v2/hero_c_sting.mp4",
  "outputs/9x16/v2/hero_d_logo.png",
  "outputs/9x16/v2/hero_d_sting.mp4",
];

export const Batch: React.FC = () => {
  const frame = useCurrentFrame();
  const btn = useEntrance(5);
  const pressed = interpolate(frame, [25, 30, 36], [1, 0.94, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const progress = interpolate(frame, [35, 165], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const done = Math.floor(progress * OUTPUTS.length);

  return (
    <SceneShell kicker="Step 4" title="Render every combination at once">
      <div style={{ position: "absolute", top: 290, left: 120, width: 760 }}>
        <div
          style={{
            padding: "26px 0",
            textAlign: "center",
            fontSize: 34,
            fontWeight: 800,
            letterSpacing: 3,
            borderRadius: 12,
            background: colors.accent,
            color: colors.bgDark,
            opacity: btn,
            transform: `scale(${pressed})`,
          }}
        >
          ▶ RENDER ALL
        </div>
        <div style={{ marginTop: 30, height: 14, background: colors.border, borderRadius: 7, overflow: "hidden" }}>
          <div style={{ width: `${progress * 100}%`, height: "100%", background: colors.accent }} />
        </div>
        <div style={{ marginTop: 16, fontSize: 24, color: colors.textMuted }}>
          {done < OUTPUTS.length
            ? `Rendering ${done + 1} / ${OUTPUTS.length}…`
            : `✓ ${OUTPUTS.length} succeeded · 0 failed`}
        </div>
        <div style={{ marginTop: 36, fontSize: 26, lineHeight: 1.6, color: colors.textMuted }}>
          Filter by format or campaign subfolder, name the output folder
          (e.g. <Mono style={{ color: colors.textPrimary }}>v2</Mono>), and{" "}
          <Mono style={{ color: colors.textPrimary }}>render_all()</Mono> pairs each hero with
          every matching overlay using its saved position.
        </div>
      </div>

      <Card style={{ position: "absolute", top: 290, left: 980, width: 820, padding: "26px 34px" }}>
        {OUTPUTS.map((path, i) => {
          const visible = i < done;
          const isVideo = path.endsWith(".mp4");
          const nine = path.includes("9x16");
          return (
            <div
              key={path}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 20,
                padding: "9px 0",
                opacity: visible ? 1 : 0.18,
              }}
            >
              <div style={{ width: 50, display: "flex", justifyContent: "center" }}>
              <HeroArt width={nine ? 32 : 50} height={nine ? 56 : 50} hue={200 + i * 30}>
                <OverlayBadge scale={0.12} label="" style={{ position: "absolute", left: 3, bottom: 3, padding: 2 }} />
              </HeroArt>
              </div>
              <Mono style={{ fontSize: 24, flex: 1 }}>{path}</Mono>
              <span style={{ fontSize: 20, color: isVideo ? colors.accent : colors.textMuted }}>
                {visible ? (isVideo ? "H.264" : "PNG") : ""}
              </span>
            </div>
          );
        })}
      </Card>
    </SceneShell>
  );
};
