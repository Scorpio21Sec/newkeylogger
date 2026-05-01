"use client";

import { Fragment, useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { ChevronDown, ChevronUp } from "lucide-react";
import { useDebounce } from "@/hooks/use-debounce";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Session } from "@/utils/types";
import { formatDateTime, formatPercent } from "@/utils/format";

type Props = {
  sessions: Session[];
  globalSearch: string;
};

type SortKey = "user" | "keystrokes" | "typingSpeed" | "errorRate";

const pageSize = 6;

export function SessionsTable({ sessions, globalSearch }: Props) {
  const [localSearch, setLocalSearch] = useState("");
  const [page, setPage] = useState(1);
  const [expandedRows, setExpandedRows] = useState<string[]>([]);
  const [sortBy, setSortBy] = useState<SortKey>("keystrokes");
  const [ascending, setAscending] = useState(false);

  const debouncedSearch = useDebounce(`${globalSearch} ${localSearch}`.trim(), 300);

  const processedSessions = useMemo(() => {
    const query = debouncedSearch.toLowerCase();

    const filtered = sessions.filter((session) => {
      if (!query) {
        return true;
      }
      return [session.user, session.app, session.device].some((value) =>
        value.toLowerCase().includes(query),
      );
    });

    filtered.sort((a, b) => {
      const left = a[sortBy];
      const right = b[sortBy];

      if (typeof left === "string" && typeof right === "string") {
        return ascending ? left.localeCompare(right) : right.localeCompare(left);
      }

      const numericSort = Number(left) - Number(right);
      return ascending ? numericSort : -numericSort;
    });

    return filtered;
  }, [sessions, debouncedSearch, sortBy, ascending]);

  const totalPages = Math.max(1, Math.ceil(processedSessions.length / pageSize));
  const safePage = Math.min(page, totalPages);
  const pagedData = processedSessions.slice((safePage - 1) * pageSize, safePage * pageSize);

  const toggleSort = (key: SortKey) => {
    setPage(1);
    setSortBy((current) => {
      if (current === key) {
        setAscending((state) => !state);
        return current;
      }
      setAscending(false);
      return key;
    });
  };

  return (
    <Card data-animate="section">
      <div className="mb-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <h3 className="text-base font-semibold">Active sessions</h3>
        <Input
          placeholder="Filter table"
          value={localSearch}
          onChange={(event) => {
            setLocalSearch(event.target.value);
            setPage(1);
          }}
          className="max-w-sm"
        />
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[720px] border-separate border-spacing-y-2 text-sm">
          <thead>
            <tr className="text-left text-slate-400">
              <th className="px-3 py-2">Session</th>
              <th className="px-3 py-2">
                <button onClick={() => toggleSort("user")}>User</button>
              </th>
              <th className="px-3 py-2">
                <button onClick={() => toggleSort("keystrokes")}>Keystrokes</button>
              </th>
              <th className="px-3 py-2">
                <button onClick={() => toggleSort("typingSpeed")}>Speed</button>
              </th>
              <th className="px-3 py-2">
                <button onClick={() => toggleSort("errorRate")}>Error</button>
              </th>
              <th className="px-3 py-2">Started</th>
            </tr>
          </thead>
          <tbody>
            <AnimatePresence initial={false}>
              {pagedData.map((session, index) => {
                const expanded = expandedRows.includes(session.id);

                return (
                  <Fragment key={session.id}>
                    <motion.tr
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 8 }}
                      transition={{ delay: index * 0.05 }}
                      className="rounded-2xl bg-white/5 transition hover:bg-white/10"
                    >
                      <td className="px-3 py-3">
                        <button
                          className="inline-flex items-center gap-2"
                          onClick={() => {
                            setExpandedRows((rows) =>
                              expanded ? rows.filter((item) => item !== session.id) : [...rows, session.id],
                            );
                          }}
                        >
                          {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                          {session.id}
                        </button>
                      </td>
                      <td className="px-3 py-3">{session.user}</td>
                      <td className="px-3 py-3">{session.keystrokes}</td>
                      <td className="px-3 py-3">{session.typingSpeed.toFixed(1)} WPM</td>
                      <td className="px-3 py-3">{formatPercent(session.errorRate)}</td>
                      <td className="px-3 py-3">{formatDateTime(session.startedAt)}</td>
                    </motion.tr>
                    <AnimatePresence>
                      {expanded ? (
                        <motion.tr
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: "auto" }}
                          exit={{ opacity: 0, height: 0 }}
                        >
                          <td colSpan={6} className="px-3 pb-2 text-slate-300">
                            <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-3">
                              Device: {session.device} | App: {session.app} | Ended: {formatDateTime(session.endedAt)}
                            </div>
                          </td>
                        </motion.tr>
                      ) : null}
                    </AnimatePresence>
                  </Fragment>
                );
              })}
            </AnimatePresence>
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex items-center justify-between text-sm text-slate-300">
        <p>
          Page {safePage} of {totalPages}
        </p>
        <div className="flex gap-2">
          <button
            className="rounded-xl border border-white/10 px-3 py-1 hover:bg-white/10 disabled:opacity-50"
            disabled={safePage <= 1}
            onClick={() => setPage((prev) => Math.max(1, prev - 1))}
          >
            Previous
          </button>
          <button
            className="rounded-xl border border-white/10 px-3 py-1 hover:bg-white/10 disabled:opacity-50"
            disabled={safePage >= totalPages}
            onClick={() => setPage((prev) => Math.min(totalPages, prev + 1))}
          >
            Next
          </button>
        </div>
      </div>
    </Card>
  );
}
