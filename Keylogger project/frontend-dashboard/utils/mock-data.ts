import { KeyLog, Session, Stats } from "@/utils/types";

const now = Date.now();

export const mockStats: Stats = {
  totalKeystrokes: 192430,
  activeSessions: 18,
  typingSpeed: 73.2,
  errorRate: 3.9,
  activityTrend: Array.from({ length: 12 }).map((_, index) => ({
    timestamp: `${index + 8}:00`,
    value: 600 + Math.round(Math.random() * 420),
  })),
  sessionComparison: [
    { name: "S-210", keystrokes: 1390 },
    { name: "S-211", keystrokes: 1674 },
    { name: "S-212", keystrokes: 1255 },
    { name: "S-213", keystrokes: 1850 },
  ],
  keyDistribution: [
    { name: "Letters", value: 56 },
    { name: "Numbers", value: 14 },
    { name: "Symbols", value: 11 },
    { name: "Whitespace", value: 19 },
  ],
};

export const mockSessions: Session[] = Array.from({ length: 16 }).map((_, index) => {
  const sessionStart = new Date(now - index * 1000 * 60 * 28);
  const sessionEnd = new Date(sessionStart.getTime() + 1000 * 60 * (12 + index));

  return {
    id: `S-${210 + index}`,
    user: ["Ari", "Mina", "Luca", "Noah"][index % 4],
    startedAt: sessionStart.toISOString(),
    endedAt: sessionEnd.toISOString(),
    keystrokes: 900 + index * 112,
    typingSpeed: 58 + (index % 6) * 3.6,
    errorRate: 2.5 + (index % 5) * 0.8,
    device: index % 2 === 0 ? "MacBook Pro" : "Windows Workstation",
    app: ["VS Code", "Chrome", "Figma", "Terminal"][index % 4],
  };
});

export const mockLogs: KeyLog[] = Array.from({ length: 48 }).map((_, index) => ({
  id: `L-${index + 1}`,
  timestamp: new Date(now - index * 1000 * 12).toISOString(),
  key: ["a", "space", "Backspace", "Enter", ";"][index % 5],
  app: ["VS Code", "Chrome", "Figma"][index % 3],
  sessionId: mockSessions[index % mockSessions.length].id,
  isError: index % 7 === 0,
}));
