import { cn } from "@/utils/cn";

type Props = {
  className?: string;
};

export function Skeleton({ className }: Props) {
  return (
    <div
      className={cn(
        "animate-shimmer rounded-2xl bg-gradient-to-r from-slate-800/70 via-slate-700/40 to-slate-800/70 bg-[length:200%_100%]",
        className,
      )}
    />
  );
}
