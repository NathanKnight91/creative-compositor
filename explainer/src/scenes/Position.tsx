import React from "react";
import { Easing, interpolate, useCurrentFrame } from "remotion";
import {
  Card,
  HeroArt,
  Mono,
  OverlayBadge,
  SceneShell,
  Slider,
  useEntrance,
} from "../components";
import { colors } from "../theme";

const ease = { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) } as const;

export const Position: React.FC = () => {
  const frame = useCurrentFrame();
  const panel = useEntrance(5);

  // Sliders animate, then the user hits "Save"
  const x = interpolate(frame, [30, 90], [0, 60], ease);
  const y = interpolate(frame, [70, 130], [0, 360], ease);
  const scale = interpolate(frame, [110, 160], [1, 1.4], ease);
  const scrub = interpolate(frame, [20, 170], [0, 1], ease);
  const saved = frame > 175;
  const saveFlash = interpolate(frame, [175, 185, 205], [0, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const json = useEntrance(185);

  const previewW = 520;
  const previewH = 520;

  return (
    <SceneShell kicker="Step 2" title="Position overlays with a live preview">
      <Card
        style={{
          position: "absolute",
          top: 290,
          left: 120,
          width: 560,
          padding: "36px 40px",
          opacity: panel,
          transform: `translateX(${(1 - panel) * -50}px)`,
        }}
      >
        <div style={{ fontSize: 22, color: colors.textMuted, marginBottom: 24, letterSpacing: 2 }}>
          1x1 · VIDEO OVERLAY
        </div>
        <Slider label="Frame position" value={scrub} min={0} max={1} format={(v) => `${Math.round(v * 100)}%`} />
        <Slider label="X offset" value={x} min={-200} max={400} />
        <Slider label="Y offset" value={y} min={-200} max={600} />
        <Slider label="Scale" value={scale} min={0.1} max={2} format={(v) => v.toFixed(2)} />
        <div
          style={{
            marginTop: 14,
            padding: "16px 0",
            textAlign: "center",
            fontSize: 24,
            fontWeight: 700,
            borderRadius: 10,
            color: colors.bgDark,
            background: colors.accent,
            boxShadow: `0 0 ${40 * saveFlash}px ${colors.accent}`,
            transform: `scale(${1 - saveFlash * 0.04})`,
          }}
        >
          {saved ? "✓ Saved" : "Save 1x1 Position"}
        </div>
      </Card>

      <div style={{ position: "absolute", top: 290, left: 760, opacity: panel }}>
        <HeroArt width={previewW} height={previewH} hue={235}>
          <OverlayBadge
            scale={scale}
            label="NEW SERIES"
            style={{
              position: "absolute",
              left: 30 + x * (previewW / 1080),
              top: 30 + y * (previewH / 1080),
              transformOrigin: "top left",
              // Fake an animated overlay: the badge pulses as the frame scrubber moves
              opacity: 0.6 + 0.4 * Math.abs(Math.sin(scrub * Math.PI * 2)),
            }}
          />
        </HeroArt>
        <div style={{ textAlign: "center", fontSize: 22, color: colors.textMuted, marginTop: 14 }}>
          Live preview · first frame via FFmpeg
        </div>
      </div>

      <Card
        style={{
          position: "absolute",
          top: 290,
          left: 1360,
          width: 440,
          padding: "30px 34px",
          opacity: json,
          transform: `translateY(${(1 - json) * 30}px)`,
        }}
      >
        <div style={{ fontSize: 22, color: colors.textMuted, marginBottom: 16 }}>config.json</div>
        <pre style={{ margin: 0, fontSize: 24, lineHeight: 1.5 }}>
          <Mono>
            <span style={{ color: colors.textMuted }}>{"{"}</span>
            {"\n  "}
            <span style={{ color: colors.accent }}>"1x1_video"</span>: {"{"}
            {"\n    "}"x": {Math.round(x)},
            {"\n    "}"y": {Math.round(y)},
            {"\n    "}"scale": {scale.toFixed(1)},
            {"\n    "}"loop_count": 1
            {"\n  }"}
            <span style={{ color: colors.textMuted }}>{"\n}"}</span>
          </Mono>
        </pre>
        <div style={{ fontSize: 22, color: colors.textMuted, marginTop: 20, lineHeight: 1.4 }}>
          Remembered per format and per overlay type.
        </div>
      </Card>
    </SceneShell>
  );
};
