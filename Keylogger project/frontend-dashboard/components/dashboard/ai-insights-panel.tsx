import { Sparkles } from "lucide-react";
import { Card } from "@/components/ui/card";

type Props = {
  speed: number;
  errorRate: number;
};

export function AIInsightsPanel({ speed, errorRate }: Props) {
  const status = speed > 65 && errorRate < 5 ? "excellent" : "improving";

  return (
    <Card data-animate="section" className="relative overflow-hidden">
      <div className="absolute -right-20 -top-20 h-52 w-52 rounded-full bg-cyan-400/20 blur-3xl" />
      <div className="relative">
        <div className="mb-3 inline-flex items-center gap-2 rounded-full bg-cyan-400/15 px-3 py-1 text-xs text-cyan-200 ring-1 ring-cyan-300/30">
          <Sparkles size={14} />
          AI Insights
        </div>
        <h3 className="text-lg font-semibold">Typing pattern summary</h3>
        <p className="mt-2 text-sm text-slate-300">
          Your current performance profile is <span className="font-semibold text-cyan-200">{status}</span>.
          Average speed is {speed.toFixed(1)} WPM while error rate remains at {errorRate.toFixed(1)}%.
        </p>
      </div>
    </Card>
  );
}
