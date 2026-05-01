"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, Keyboard, LayoutDashboard, LogOut, Settings } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/utils/cn";
import { Button } from "@/components/ui/button";

const items = [
  { href: "/", label: "Overview", icon: LayoutDashboard },
  { href: "/", label: "Keystrokes", icon: Keyboard },
  { href: "/", label: "Reports", icon: BarChart3 },
  { href: "/", label: "Settings", icon: Settings },
];

type Props = {
  collapsed: boolean;
  onToggle: () => void;
};

export function Sidebar({ collapsed, onToggle }: Props) {
  const pathname = usePathname();

  return (
    <motion.aside
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1, width: collapsed ? 90 : 250 }}
      transition={{ type: "spring", damping: 20, stiffness: 160 }}
      className="sticky top-0 h-screen border-r border-white/10 bg-slate-900/70 p-4 backdrop-blur-xl"
    >
      <div className="mb-8 flex items-center justify-between">
        <div className={cn("font-semibold tracking-tight", collapsed && "sr-only")}>
          VelocityBoard
        </div>
        <Button variant="ghost" className="h-9 w-9 p-0" onClick={onToggle}>
          {collapsed ? ">" : "<"}
        </Button>
      </div>

      <nav className="space-y-2">
        {items.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.label}
              href={item.href}
              className={cn(
                "group relative flex items-center gap-3 rounded-2xl px-3 py-2 text-sm text-slate-300 transition hover:bg-white/10",
                active && "bg-cyan-400/20 text-cyan-100",
              )}
            >
              {active ? (
                <motion.span
                  layoutId="activeRoute"
                  className="absolute inset-0 rounded-2xl border border-cyan-300/40"
                />
              ) : null}
              <Icon size={16} />
              <span className={cn(collapsed && "hidden")}>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <Button variant="ghost" className="absolute bottom-4 left-4 right-4 justify-start">
        <LogOut size={16} />
        <span className={cn(collapsed && "hidden")}>Sign out</span>
      </Button>
    </motion.aside>
  );
}
