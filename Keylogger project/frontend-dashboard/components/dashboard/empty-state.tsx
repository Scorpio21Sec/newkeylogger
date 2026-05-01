import { Inbox } from "lucide-react";
import { Card } from "@/components/ui/card";

export function EmptyState() {
  return (
    <Card className="flex flex-col items-center justify-center gap-3 py-16 text-center">
      <Inbox className="text-slate-300" size={26} />
      <h3 className="text-lg font-semibold">No analytics data yet</h3>
      <p className="max-w-sm text-sm text-slate-300">
        We could not find recent keylogger sessions. Keep typing and this dashboard will auto-refresh.
      </p>
    </Card>
  );
}
