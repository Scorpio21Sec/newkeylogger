"use client";

import { create } from "zustand";
import { dashboardApi } from "@/utils/api";
import { KeyLog, Session, Stats } from "@/utils/types";

type DashboardState = {
  logs: KeyLog[];
  sessions: Session[];
  stats: Stats | null;
  loading: boolean;
  error: string | null;
  fetchAll: () => Promise<void>;
};

export const useDashboardStore = create<DashboardState>((set) => ({
  logs: [],
  sessions: [],
  stats: null,
  loading: false,
  error: null,
  fetchAll: async () => {
    set((state) => ({ ...state, loading: true, error: null }));

    try {
      const [stats, logs, sessions] = await Promise.all([
        dashboardApi.getStats(),
        dashboardApi.getLogs(),
        dashboardApi.getSessions(),
      ]);

      set((state) => ({
        ...state,
        stats,
        logs,
        sessions,
        loading: false,
      }));
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unable to load analytics data";

      set((state) => ({
        ...state,
        loading: false,
        error: message,
      }));
    }
  },
}));
