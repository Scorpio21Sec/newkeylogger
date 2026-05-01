export type TrendPoint = {
  timestamp: string;
  value: number;
};

export type Session = {
  id: string;
  user: string;
  startedAt: string;
  endedAt: string;
  keystrokes: number;
  typingSpeed: number;
  errorRate: number;
  device: string;
  app: string;
};

export type KeyLog = {
  id: string;
  timestamp: string;
  key: string;
  app: string;
  sessionId: string;
  isError: boolean;
};

export type Stats = {
  totalKeystrokes: number;
  activeSessions: number;
  typingSpeed: number;
  errorRate: number;
  activityTrend: TrendPoint[];
  sessionComparison: Array<{ name: string; keystrokes: number }>;
  keyDistribution: Array<{ name: string; value: number }>;
};

export type ApiEnvelope<T> = {
  data: T;
  message?: string;
};
