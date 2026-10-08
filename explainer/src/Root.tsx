import { Composition } from "remotion";
import { Explainer, EXPLAINER_DURATION } from "./Explainer";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Explainer"
    component={Explainer}
    durationInFrames={EXPLAINER_DURATION}
    fps={30}
    width={1920}
    height={1080}
  />
);
