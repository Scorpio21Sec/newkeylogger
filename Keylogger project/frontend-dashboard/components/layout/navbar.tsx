"use client";

import { Bell, Search } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { ThemeToggle } from "@/components/layout/theme-toggle";
import { Button } from "@/components/ui/button";

type Props = {
  search: string;
  onSearchChange: (value: string) => void;
};

export function Navbar({ search, onSearchChange }: Props) {
  return (
    <header className="sticky top-0 z-30 border-b border-white/10 bg-slate-950/65 px-4 py-3 backdrop-blur-xl md:px-6">
      <div className="flex flex-wrap items-center gap-3">
        <div className="relative min-w-[220px] flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
          <Input
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search sessions, apps, users"
            className="pl-9"
          />
        </div>
        <Badge status="online">Live ingesting</Badge>
        <Button variant="ghost" className="h-10 w-10 rounded-full p-0">
          <Bell size={16} />
        </Button>
        <ThemeToggle />
        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-cyan-300 to-blue-500" />
      </div>
    </header>
  );
}
