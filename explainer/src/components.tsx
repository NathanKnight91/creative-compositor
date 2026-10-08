import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { colors, fonts } from "./theme";

/** Fades a whole scene in and out so scenes can sit back to back. */
export const SceneShell: React.FC<{
  kicker?: string;
  title?: string;
  children: React.ReactNode;
}> = ({ kicker, title, children }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const opacity = interpolate(
    frame,
    [0, 12, durationInFrames - 12, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const titleY = interpolate(frame, [0, 20], [24, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.bgDark,
        fontFamily: fonts.sans,
        color: colors.textPrimary,
        opacity,
      }}
    >
      <GridBackdrop />
      {title ? (
        <div
          style={{
            position: "absolute",
            top: 80,
            left: 120,
            transform: `translateY(${titleY}px)`,
          }}
        >
          {kicker ? (
            <div
              style={{
                color: colors.accent,
                fontSize: 26,
                fontWeight: 700,
                letterSpacing: 4,
                textTransform: "uppercase",
                marginBottom: 12,
              }}
            >
              {kicker}
            </div>
          ) : null}
          <div style={{ fontSize: 64, fontWeight: 800, letterSpacing: -1 }}>
            {title}
          </div>
        </div>
      ) : null}
      {children}
    </AbsoluteFill>
  );
};

const GridBackdrop: React.FC = () => (
  <AbsoluteFill
    style={{
      backgroundImage: `linear-gradient(${colors.border}33 1px, transparent 1px), linear-gradient(90deg, ${colors.border}33 1px, transparent 1px)`,
      backgroundSize: "80px 80px",
    }}
  />
);

/** Lucide-style layers icon, same as the app header. */
export const LayersIcon: React.FC<{ size?: number; color?: string }> = ({
  size = 48,
  color = colors.accent,
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke={color}
    strokeWidth={2}
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z" />
    <path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65" />
    <path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65" />
  </svg>
);

/** Spring-driven entrance: returns 0→1 starting at `delay` frames. */
export const useEntrance = (delay = 0, damping = 16) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - delay, fps, config: { damping } });
};

export const Card: React.FC<{
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({ style, children }) => (
  <div
    style={{
      background: colors.bgCard,
      border: `1px solid ${colors.border}`,
      borderRadius: 16,
      ...style,
    }}
  >
    {children}
  </div>
);

/** Stylised "hero image": a sky/landscape gradient standing in for campaign art. */
export const HeroArt: React.FC<{
  width: number;
  height: number;
  hue?: number;
  children?: React.ReactNode;
}> = ({ width, height, hue = 250, children }) => (
  <div
    style={{
      width,
      height,
      position: "relative",
      overflow: "hidden",
      borderRadius: 10,
      background: `linear-gradient(160deg, hsl(${hue} 60% 35%), hsl(${
        hue + 40
      } 55% 18%))`,
      boxShadow: "0 20px 60px rgba(0,0,0,0.5)",
    }}
  >
    <div
      style={{
        position: "absolute",
        width: width * 0.45,
        height: width * 0.45,
        borderRadius: "50%",
        right: width * 0.1,
        top: height * 0.12,
        background: `radial-gradient(circle, hsl(${hue - 200} 90% 70%), hsl(${
          hue - 200
        } 90% 50% / 0))`,
      }}
    />
    <div
      style={{
        position: "absolute",
        left: -width * 0.2,
        right: -width * 0.2,
        bottom: -height * 0.15,
        height: height * 0.5,
        borderRadius: "50% 50% 0 0",
        background: `hsl(${hue + 60} 40% 12%)`,
      }}
    />
    {children}
  </div>
);

/** A generic brand overlay (logo lock-up) used in the compositing demos. */
export const OverlayBadge: React.FC<{
  scale?: number;
  label?: string;
  style?: React.CSSProperties;
}> = ({ scale = 1, label = "NEW SERIES", style }) => (
  <div
    style={{
      display: "flex",
      alignItems: "center",
      gap: 10 * scale,
      padding: `${10 * scale}px ${18 * scale}px`,
      background: colors.accent,
      color: colors.bgDark,
      fontWeight: 900,
      fontSize: 22 * scale,
      letterSpacing: 2 * scale,
      borderRadius: 6 * scale,
      whiteSpace: "nowrap",
      boxShadow: "0 6px 20px rgba(0,0,0,0.4)",
      ...style,
    }}
  >
    <LayersIcon size={26 * scale} color={colors.bgDark} />
    {label}
  </div>
);

export const Slider: React.FC<{
  label: string;
  value: number;
  min: number;
  max: number;
  format?: (v: number) => string;
}> = ({ label, value, min, max, format = (v) => String(Math.round(v)) }) => {
  const pct = (value - min) / (max - min);
  return (
    <div style={{ marginBottom: 26 }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          fontSize: 22,
          color: colors.textMuted,
          marginBottom: 10,
        }}
      >
        <span>{label}</span>
        <span style={{ color: colors.textPrimary, fontFamily: fonts.mono }}>
          {format(value)}
        </span>
      </div>
      <div
        style={{
          height: 6,
          background: colors.border,
          borderRadius: 3,
          position: "relative",
        }}
      >
        <div
          style={{
            width: `${pct * 100}%`,
            height: "100%",
            background: colors.accent,
            borderRadius: 3,
          }}
        />
        <div
          style={{
            position: "absolute",
            left: `calc(${pct * 100}% - 11px)`,
            top: -8,
            width: 22,
            height: 22,
            borderRadius: "50%",
            background: colors.accentHover,
            border: `3px solid ${colors.bgDark}`,
          }}
        />
      </div>
    </div>
  );
};

export const Mono: React.FC<{
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ children, style }) => (
  <span style={{ fontFamily: fonts.mono, ...style }}>{children}</span>
);
