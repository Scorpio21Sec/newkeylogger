"use client";

import { Bell, Search, LogOut } from "lucide-react";
import { useRouter } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { ThemeToggle } from "@/components/layout/theme-toggle";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/store/auth-store";

type Props = {
  search: string;
  onSearchChange: (value: string) => void;
};

export function Navbar({ search, onSearchChange }: Props) {
  const router = useRouter();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

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
        {user && (
          <div className="flex items-center gap-2 ml-2 pl-2 border-l border-white/10">
            <div className="flex flex-col items-end">
              <p className="text-xs font-medium text-slate-200">{user.name}</p>
              <p className="text-xs text-slate-400">{user.role}</p>
            </div>
            <div className="h-10 w-10 rounded-full bg-gradient-to-br from-cyan-300 to-blue-500" />
            <Button
              variant="ghost"
              className="h-10 w-10 rounded-full p-0"
              onClick={handleLogout}
              title="Logout"
            >
              <LogOut size={16} />
            </Button>
          </div>
        )}
      </div>
    </header>
  );
}
