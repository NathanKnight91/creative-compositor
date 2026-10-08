import React from "react";
import { Card, LayersIcon, Mono, SceneShell, useEntrance } from "../components";
import { colors } from "../theme";

const CMDS = ["pip install -r requirements.txt", "streamlit run app.py"];

export const Outro: React.FC = () => {
  const head = useEntrance(0);
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
        <div style={{ display: "flex", alignItems: "center", gap: 28, opacity: head }}>
          <LayersIcon size={96} />
          <div style={{ fontSize: 84, fontWeight: 900, letterSpacing: -2 }}>Creative Compositor</div>
        </div>
        <Card style={{ marginTop: 60, padding: "34px 50px", minWidth: 760 }}>
          {CMDS.map((cmd, i) => {
            const s = useEntrance(15 + i * 15);
            return (
              <div key={cmd} style={{ fontSize: 36, padding: "8px 0", opacity: s }}>
                <Mono>
                  <span style={{ color: colors.accent }}>$ </span>
                  {cmd}
                </Mono>
              </div>
            );
          })}
        </Card>
        <div style={{ marginTop: 40, fontSize: 30, color: colors.textMuted, opacity: useEntrance(50) }}>
          Opens at <Mono style={{ color: colors.textPrimary }}>localhost:8501</Mono> · FFmpeg required for video overlays
        </div>
      </div>
    </SceneShell>
  );
};
