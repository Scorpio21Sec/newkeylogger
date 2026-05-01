"use client";

import { ReactNode, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Navbar } from "@/components/layout/navbar";
import { Sidebar } from "@/components/layout/sidebar";

type Props = {
  search: string;
  onSearchChange: (value: string) => void;
  children: ReactNode;
};

export function DashboardShell({ search, onSearchChange, children }: Props) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="relative flex min-h-screen bg-slate-950 text-slate-100">
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed((prev) => !prev)} />
      <div className="flex min-h-screen flex-1 flex-col overflow-hidden">
        <Navbar search={search} onSearchChange={onSearchChange} />
        <AnimatePresence mode="wait">
          <motion.main
            key="dashboard-content"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.35 }}
            className="flex-1 overflow-y-auto px-4 py-5 md:px-6 md:py-6"
          >
            {children}
          </motion.main>
        </AnimatePresence>
      </div>
    </div>
  );
}
