import { InputHTMLAttributes } from "react";
import { cn } from "@/utils/cn";

export function Input({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        "h-10 w-full rounded-2xl border border-white/10 bg-white/5 px-4 text-sm text-slate-100 outline-none placeholder:text-slate-400",
        "transition focus:border-cyan-300/60 focus:shadow-[0_0_0_3px_rgba(34,211,238,0.2)]",
        className,
      )}
      {...props}
    />
  );
}
