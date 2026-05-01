import { HTMLAttributes } from "react";
import { cn } from "@/utils/cn";

export function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "relative rounded-2xl border border-white/10 bg-white/5 p-5 shadow-[0_20px_40px_rgba(2,6,23,0.35)] backdrop-blur-xl",
        "before:pointer-events-none before:absolute before:inset-0 before:rounded-2xl before:p-px before:[background:linear-gradient(135deg,rgba(56,189,248,0.6),rgba(99,102,241,0.15),rgba(45,212,191,0.4))] before:[mask:linear-gradient(#fff_0_0)_content-box,linear-gradient(#fff_0_0)] before:[mask-composite:exclude]",
        className,
      )}
      {...props}
    />
  );
}
