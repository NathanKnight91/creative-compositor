import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { Architecture } from "./scenes/Architecture";
import { Batch } from "./scenes/Batch";
import { Engine } from "./scenes/Engine";
import { Inputs } from "./scenes/Inputs";
import { Intro } from "./scenes/Intro";
import { Outro } from "./scenes/Outro";
import { Position } from "./scenes/Position";
import { Problem } from "./scenes/Problem";
import { TextTool } from "./scenes/TextTool";
import { colors } from "./theme";

// Scene order and length (frames at 30fps). Total length is derived from this list.
const SCENES: { Component: React.FC; duration: number }[] = [
  { Component: Intro, duration: 120 },
  { Component: Problem, duration: 180 },
  { Component: Inputs, duration: 180 },
  { Component: Position, duration: 260 },
  { Component: Engine, duration: 210 },
  { Component: TextTool, duration: 210 },
  { Component: Batch, duration: 210 },
  { Component: Architecture, duration: 210 },
  { Component: Outro, duration: 150 },
];

export const EXPLAINER_DURATION = SCENES.reduce((sum, s) => sum + s.duration, 0);

export const Explainer: React.FC = () => {
  let from = 0;
  return (
    <AbsoluteFill style={{ backgroundColor: colors.bgDark }}>
      {SCENES.map(({ Component, duration }, i) => {
        const seq = (
          <Sequence key={i} from={from} durationInFrames={duration}>
            <Component />
          </Sequence>
        );
        from += duration;
        return seq;
      })}
    </AbsoluteFill>
  );
};
