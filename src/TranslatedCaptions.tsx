import { useCurrentFrame, interpolate, AbsoluteFill } from "remotion";
import { useEffect, useState } from "react";

type Segment = {
  start: number;
  end: number;
  translated: string;
};

type BlurBox = {
  x: number;
  y: number;
  width: number;
  height: number;
};

export const TranslatedCaptions = () => {
  const [segments, setSegments] = useState<Segment[]>([]);
  const [blurBox, setBlurBox] = useState<BlurBox | null>(null);
  const frame = useCurrentFrame();
  const fps = 30;

  useEffect(() => {
    fetch("/translated_segments.json")
      .then((res) => res.json())
      .then(setSegments);

    fetch("/blur_box.json")
      .then((res) => res.json())
      .then(setBlurBox);
  }, []);

  if (!blurBox) return null;

  return (
    <AbsoluteFill>
      {/* Rectangle flou */}
      <div
        style={{
          position: "absolute",
          left: blurBox.x,
          top: blurBox.y,
          width: blurBox.width,
          height: blurBox.height,
          backdropFilter: "blur(16px)",
          backgroundColor: "rgb(254, 157, 157)",
          zIndex: 1,
        }}
      />
      {/* Sous-titre par-dessus */}
      <div
        style={{
          position: "absolute",
          left: blurBox.x,
          top: blurBox.y,
          width: blurBox.width,
          height: blurBox.height,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 2,
          pointerEvents: "none",
        }}
      >
        {segments.map((seg, i) => {
          const start = Math.floor(seg.start * fps);
          const end = Math.floor(seg.end * fps);
          if (frame < start || frame > end) return null;
          const opacity = interpolate(frame, [start, end], [1, 0], { extrapolateRight: "clamp" });
          return (
            <span
              key={i}
              style={{
                fontSize: 48,
                color: "white",
                background: "rgb(254, 157, 157)",
                borderRadius: 12,
                padding: "10px 20px",
                opacity,
                pointerEvents: "none",
              }}
            >
              {seg.translated}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
