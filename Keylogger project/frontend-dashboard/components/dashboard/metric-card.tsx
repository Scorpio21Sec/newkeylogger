"use client";

import { useEffect, useMemo, useState } from "react";
import { motion, useMotionValue, useTransform } from "framer-motion";
import { Card } from "@/components/ui/card";
import { formatNumber, formatPercent } from "@/utils/format";

type Props = {
  title: string;
  value: number;
  unit?: "number" | "percent";
  delta: string;
};

export function MetricCard({ title, value, unit = "number", delta }: Props) {
  const [displayValue, setDisplayValue] = useState(0);
  const rotateX = useMotionValue(0);
  const rotateY = useMotionValue(0);
  const glow = useTransform(rotateX, [-8, 8], [0.2, 0.55]);

  useEffect(() => {
    let frame = 0;
    let start = 0;
    const duration = 700;

    const animate = (timestamp: number) => {
      if (!start) {
        start = timestamp;
      }
      const progress = Math.min((timestamp - start) / duration, 1);
      setDisplayValue(Math.round(progress * value));

      if (progress < 1) {
        frame = requestAnimationFrame(animate);
      }
    };

    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, [value]);

  const renderedValue = useMemo(() => {
    return unit === "percent" ? formatPercent(displayValue) : formatNumber(displayValue);
  }, [displayValue, unit]);

  return (
    <motion.div
      whileHover={{ y: -4 }}
      style={{ rotateX, rotateY, transformStyle: "preserve-3d" }}
      onMouseMove={(event) => {
        const rect = event.currentTarget.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        rotateY.set(((x / rect.width) * 2 - 1) * 6);
        rotateX.set(((y / rect.height) * 2 - 1) * -6);
      }}
      onMouseLeave={() => {
        rotateX.set(0);
        rotateY.set(0);
      }}
      className="h-full"
    >
      <Card className="h-full">
        <motion.div style={{ opacity: glow }} className="absolute inset-0 rounded-2xl bg-cyan-400/20 blur-2xl" />
        <p className="text-xs uppercase tracking-[0.18em] text-slate-300">{title}</p>
        <p className="mt-2 text-3xl font-semibold">{renderedValue}</p>
        <p className="mt-2 text-sm text-emerald-300">{delta}</p>
      </Card>
    </motion.div>
  );
}
