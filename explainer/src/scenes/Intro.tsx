import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { LayersIcon, SceneShell, useEntrance } from "../components";
import { colors } from "../theme";

export const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const icon = useEntrance(0, 12);
  const title = useEntrance(10);
  const tagline = useEntrance(25);
  const underline = interpolate(frame, [30, 60], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <SceneShell>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div style={{ transform: `scale(${icon}) rotate(${(1 - icon) * -90}deg)` }}>
          <LayersIcon size={160} />
        </div>
        <div
          style={{
            fontSize: 120,
            fontWeight: 900,
            letterSpacing: -3,
            marginTop: 30,
            opacity: title,
            transform: `translateY(${(1 - title) * 40}px)`,
          }}
        >
          Creative Compositor
        </div>
        <div
          style={{
            height: 6,
            width: 520 * underline,
            background: colors.accent,
            borderRadius: 3,
            marginTop: 16,
          }}
        />
        <div
          style={{
            fontSize: 40,
            color: colors.textMuted,
            marginTop: 36,
            opacity: tagline,
            transform: `translateY(${(1 - tagline) * 20}px)`,
          }}
        >
          Hero images + overlays → every social format, in one batch
        </div>
      </div>
    </SceneShell>
  );
};
