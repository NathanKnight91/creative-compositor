import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { Card, Mono, SceneShell, useEntrance } from "../components";
import { colors } from "../theme";

const Pipe: React.FC<{
  delay: number;
  top: number;
  input: string;
  engine: string;
  detail: string;
  output: string;
}> = ({ delay, top, input, engine, detail, output }) => {
  const frame = useCurrentFrame();
  const a = useEntrance(delay);
  const b = useEntrance(delay + 15);
  const c = useEntrance(delay + 30);
  // Packet travelling along the pipe
  const t = interpolate((frame - delay - 30) % 60, [0, 60], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const showPacket = frame > delay + 40;

  const box = (s: number): React.CSSProperties => ({
    opacity: s,
    transform: `scale(${0.8 + 0.2 * s})`,
  });

  return (
    <div style={{ position: "absolute", top, left: 120, width: 1680, height: 220 }}>
      <div
        style={{
          position: "absolute",
          top: 108,
          left: 320,
          width: 1040,
          height: 4,
          background: colors.border,
        }}
      />
      {showPacket ? (
        <div
          style={{
            position: "absolute",
            top: 100,
            left: 320 + t * 1020,
            width: 20,
            height: 20,
            borderRadius: "50%",
            background: colors.accent,
            boxShadow: `0 0 20px ${colors.accent}`,
          }}
        />
      ) : null}
      <Card style={{ position: "absolute", left: 0, top: 40, width: 320, padding: 28, ...box(a) }}>
        <div style={{ fontSize: 20, color: colors.textMuted }}>INPUT</div>
        <div style={{ fontSize: 30, fontWeight: 700, marginTop: 8 }}>{input}</div>
      </Card>
      <Card
        style={{
          position: "absolute",
          left: 560,
          top: 0,
          width: 560,
          padding: 30,
          border: `2px solid ${colors.accent}`,
          background: colors.bgElevated,
          ...box(b),
        }}
      >
        <div style={{ fontSize: 34, fontWeight: 800, color: colors.accent }}>{engine}</div>
        <div style={{ fontSize: 22, color: colors.textMuted, marginTop: 12, lineHeight: 1.5 }}>
          <Mono>{detail}</Mono>
        </div>
      </Card>
      <Card style={{ position: "absolute", left: 1360, top: 40, width: 320, padding: 28, ...box(c) }}>
        <div style={{ fontSize: 20, color: colors.textMuted }}>OUTPUT</div>
        <div style={{ fontSize: 30, fontWeight: 700, marginTop: 8 }}>{output}</div>
      </Card>
    </div>
  );
};

export const Engine: React.FC = () => (
  <SceneShell kicker="Step 3 · compositor.py" title="Two rendering paths, one engine">
    <Pipe
      delay={15}
      top={290}
      input="Hero + PNG"
      engine="Pillow alpha composite"
      detail="scale → offset (x, y) → paste with transparency"
      output=".png"
    />
    <Pipe
      delay={70}
      top={600}
      input="Hero + MOV/MP4"
      engine="FFmpeg overlay filter"
      detail="loop hero · stream_loop overlay × N → libx264, yuv420p, +faststart"
      output=".mp4 (H.264)"
    />
  </SceneShell>
);
