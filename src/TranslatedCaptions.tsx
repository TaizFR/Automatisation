import { useCurrentFrame, interpolate, AbsoluteFill } from "remotion";
import { useEffect, useState } from "react";

type Segment = {
  start: number;
  end: number;
  translated: string;
};

export const TranslatedCaptions = () => {
  const [segments, setSegments] = useState<Segment[]>([]);
  const frame = useCurrentFrame();
  const fps = 30;

  useEffect(() => {
    fetch("/translated_segments.json")
      .then((res) => res.json())
      .then(setSegments);
  }, []);

  return (
    <AbsoluteFill>
      {/* ✅ Zone floutée en bas */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          height: 120,
          width: "100%",
          backdropFilter: "blur(16px)",
          backgroundColor: "rgba(0,0,0,0.3)",
          zIndex: 1,
        }}
      />

      {/* ✅ Sous-titres par-dessus */}
      <div style={{
        position: "absolute",
        bottom: 30,
        width: "100%",
        textAlign: "center",
        zIndex: 2
      }}>
        {segments.map((seg, i) => {
          const start = Math.floor(seg.start * fps);
          const end = Math.floor(seg.end * fps);
          if (frame < start || frame > end) return null;

          const opacity = interpolate(
            frame,
            [start, end],
            [1, 0],
            { extrapolateRight: "clamp" }
          );

          return (
            <div
              key={i}
              style={{
                fontSize: 48,
                color: "white",
                background: "rgba(0,0,0,0.6)",
                borderRadius: 12,
                padding: "10px 20px",
                display: "inline-block",
                opacity,
              }}
            >
              {seg.translated}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
