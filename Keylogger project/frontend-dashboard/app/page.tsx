"use client";

import dynamic from "next/dynamic";
import { useEffect, useRef, useState } from "react";
import gsap from "gsap";
import { useShallow } from "zustand/react/shallow";
import { toast } from "sonner";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { MetricCard } from "@/components/dashboard/metric-card";
import { SessionsTable } from "@/components/dashboard/sessions-table";
import { EmptyState } from "@/components/dashboard/empty-state";
import { AIInsightsPanel } from "@/components/dashboard/ai-insights-panel";
import { DashboardLoading } from "@/components/dashboard/dashboard-loading";
import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";
import { useDashboardStore } from "@/store/dashboard-store";
import { useGsapScroll } from "@/hooks/use-gsap-scroll";

const ChartsSection = dynamic(
  () => import("@/components/dashboard/charts-section").then((mod) => mod.ChartsSection),
  { ssr: false, loading: () => <DashboardLoading /> },
);

export default function Home() {
  const [search, setSearch] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const sectionRef = useRef<HTMLElement | null>(null);
  const parallaxRef = useRef<HTMLDivElement | null>(null);

  const { stats, sessions, loading, error, fetchAll } = useDashboardStore(
    useShallow((state) => ({
      stats: state.stats,
      sessions: state.sessions,
      loading: state.loading,
      error: state.error,
      fetchAll: state.fetchAll,
    })),
  );

  useGsapScroll(sectionRef);

  useEffect(() => {
    void fetchAll();
    const intervalId = window.setInterval(() => {
      void fetchAll();
    }, 10000);
    return () => {
      window.clearInterval(intervalId);
    };
  }, [fetchAll]);

  useEffect(() => {
    if (error) {
      toast.error(error);
    }
  }, [error]);

  useEffect(() => {
    if (!stats) {
      return;
    }
    toast.success("Dashboard data refreshed", { duration: 1500 });
  }, [stats]);

  useEffect(() => {
    const blob = parallaxRef.current;
    if (!blob) {
      return;
    }

    const handleMouseMove = (event: MouseEvent) => {
      const x = ((event.clientX / window.innerWidth) * 2 - 1) * 15;
      const y = ((event.clientY / window.innerHeight) * 2 - 1) * 10;
      gsap.to(blob, {
        x,
        y,
        duration: 0.45,
        ease: "power2.out",
        force3D: true,
      });
    };

    window.addEventListener("mousemove", handleMouseMove, { passive: true });
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <DashboardShell search={search} onSearchChange={setSearch}>
      <section ref={sectionRef} className="relative space-y-4">
        <div ref={parallaxRef} className="pointer-events-none absolute -right-20 -top-14 h-72 w-72 rounded-full bg-cyan-400/20 blur-3xl" />

        <div data-animate="section" className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">Typing Analytics</h1>
            <p className="text-sm text-slate-300">Live operational view of keystroke activity and session quality.</p>
          </div>
          <Button onClick={() => setModalOpen(true)}>Data source</Button>
        </div>

        {loading && !stats ? (
          <DashboardLoading />
        ) : stats ? (
          <>
            <section data-animate="section" className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
              <MetricCard title="Total keystrokes" value={stats.totalKeystrokes} delta="+12.6% vs yesterday" />
              <MetricCard title="Active sessions" value={stats.activeSessions} delta="+4 in last 10 min" />
              <MetricCard title="Typing speed" value={stats.typingSpeed} delta="+2.4 WPM trend" />
              <MetricCard title="Error rate" value={stats.errorRate} unit="percent" delta="-0.8% quality gain" />
            </section>

            <ChartsSection stats={stats} />
            <AIInsightsPanel speed={stats.typingSpeed} errorRate={stats.errorRate} />
            {sessions.length > 0 ? <SessionsTable sessions={sessions} globalSearch={search} /> : <EmptyState />}
          </>
        ) : (
          <EmptyState />
        )}

        <Modal open={modalOpen} onClose={() => setModalOpen(false)} title="API Integration">
          <p>
            This dashboard calls /api/keylogger/logs, /api/keylogger/stats, and /api/keylogger/sessions with Axios.
            Configure NEXT_PUBLIC_API_BASE_URL to point at your external backend when needed.
          </p>
        </Modal>
      </section>
    </DashboardShell>
  );
}
