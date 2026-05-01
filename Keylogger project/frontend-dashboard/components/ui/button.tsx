"use client";

import { MouseEvent, ReactNode, useState } from "react";
import { HTMLMotionProps, motion } from "framer-motion";
import { cn } from "@/utils/cn";

type Ripple = {
  id: number;
  x: number;
  y: number;
};

type Props = HTMLMotionProps<"button"> & {
  variant?: "primary" | "ghost";
};

export function Button({
  className,
  variant = "primary",
  children,
  onClick,
  ...props
}: Props) {
  const [ripples, setRipples] = useState<Ripple[]>([]);

  const handleClick = (event: MouseEvent<HTMLButtonElement>) => {
    const rect = event.currentTarget.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    setRipples((current) => [...current, { id: Date.now(), x, y }]);
    onClick?.(event);
  };

  return (
    <motion.button
      whileHover={{ scale: 1.02, y: -1 }}
      whileTap={{ scale: 0.98 }}
      className={cn(
        "relative overflow-hidden rounded-2xl px-4 py-2 text-sm font-semibold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400",
        variant === "primary" &&
          "bg-gradient-to-r from-blue-500 via-cyan-500 to-teal-400 text-white shadow-[0_12px_30px_rgba(45,212,191,0.25)]",
        variant === "ghost" &&
          "bg-white/5 text-slate-200 ring-1 ring-white/10 hover:bg-white/10",
        className,
      )}
      onClick={handleClick}
      {...props}
    >
      {ripples.map((ripple) => (
        <span
          key={ripple.id}
          className="pointer-events-none absolute h-20 w-20 animate-ripple rounded-full bg-white/35"
          style={{ left: ripple.x - 40, top: ripple.y - 40 }}
          onAnimationEnd={() => {
            setRipples((current) => current.filter((item) => item.id !== ripple.id));
          }}
        />
      ))}
      <span className="relative z-10">{children as ReactNode}</span>
    </motion.button>
  );
}
