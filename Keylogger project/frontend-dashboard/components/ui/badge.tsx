import { HTMLAttributes } from "react";
import { cn } from "@/utils/cn";

type Props = HTMLAttributes<HTMLSpanElement> & {
  status?: "online" | "warning" | "offline";
};

export function Badge({ className, status = "online", children, ...props }: Props) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-medium ring-1",
        status === "online" && "bg-emerald-400/15 text-emerald-300 ring-emerald-300/30",
        status === "warning" && "bg-amber-400/15 text-amber-200 ring-amber-300/30",
        status === "offline" && "bg-rose-400/15 text-rose-300 ring-rose-300/30",
        className,
      )}
      {...props}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-current" />
      {children}
    </span>
  );
}
