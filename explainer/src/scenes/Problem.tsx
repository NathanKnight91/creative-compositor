import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { HeroArt, OverlayBadge, SceneShell, useEntrance } from "../components";
import { colors } from "../theme";

const HEROES = [210, 250, 300, 20];
const OVERLAYS = ["NEW SERIES", "WATCH NOW", "TONIGHT 9PM"];

export const Problem: React.FC = () => {
  const frame = useCurrentFrame();
  const counter = Math.round(
    interpolate(frame, [70, 130], [0, HEROES.length * OVERLAYS.length * 2], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );
  const counterIn = useEntrance(60);

  return (
    <SceneShell kicker="The problem" title="Campaigns multiply fast">
      <div
        style={{
          position: "absolute",
          top: 300,
          left: 120,
          display: "grid",
          gridTemplateColumns: `repeat(${HEROES.length}, 240px)`,
          gap: 28,
        }}
      >
        {OVERLAYS.flatMap((label, row) =>
          HEROES.map((hue, col) => {
            const i = row * HEROES.length + col;
            const s = useEntrance(10 + i * 4);
            return (
              <div
                key={`${row}-${col}`}
                style={{ transform: `scale(${s})`, opacity: s }}
              >
                <HeroArt width={240} height={180} hue={hue}>
                  <OverlayBadge
                    scale={0.55}
                    label={label}
                    style={{ position: "absolute", left: 12, bottom: 12 }}
                  />
                </HeroArt>
              </div>
            );
          })
        )}
      </div>
      <div
        style={{
          position: "absolute",
          right: 140,
          top: 340,
          width: 560,
          opacity: counterIn,
          transform: `translateX(${(1 - counterIn) * 60}px)`,
        }}
      >
        <div style={{ fontSize: 36, color: colors.textMuted, lineHeight: 1.5 }}>
          {HEROES.length} heroes × {OVERLAYS.length} overlays × 2 formats
        </div>
        <div
          style={{
            fontSize: 220,
            fontWeight: 900,
            color: colors.accent,
            lineHeight: 1,
            marginTop: 10,
          }}
        >
          {counter}
        </div>
        <div style={{ fontSize: 36, color: colors.textMuted, marginTop: 10 }}>
          files to line up by hand.
        </div>
      </div>
    </SceneShell>
  );
};
