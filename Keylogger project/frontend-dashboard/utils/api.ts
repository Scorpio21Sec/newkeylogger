import axios, { AxiosError } from "axios";
import { ApiEnvelope, KeyLog, Session, Stats } from "@/utils/types";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL ?? "",
  timeout: 8000,
});

api.interceptors.response.use(undefined, async (error: AxiosError) => {
  const config = error.config as AxiosError["config"] & { _retryCount?: number };

  if (!config) {
    return Promise.reject(error);
  }

  const retryCount = config._retryCount ?? 0;

  if (retryCount >= 2) {
    return Promise.reject(error);
  }

  const nextRetry = retryCount + 1;
  config._retryCount = nextRetry;
  await new Promise((resolve) => setTimeout(resolve, 500 * nextRetry));
  return api(config);
});

const unwrap = <T>(response: { data: T | ApiEnvelope<T> }) => {
  const payload = response.data as T | ApiEnvelope<T>;
  if (typeof payload === "object" && payload !== null && "data" in payload) {
    return payload.data;
  }
  return payload as T;
};

export const dashboardApi = {
  async getStats() {
    const response = await api.get<Stats | ApiEnvelope<Stats>>("/api/keylogger/stats");
    return unwrap<Stats>(response);
  },
  async getLogs() {
    const response = await api.get<KeyLog[] | ApiEnvelope<KeyLog[]>>(
      "/api/keylogger/logs",
    );
    return unwrap<KeyLog[]>(response);
  },
  async getSessions() {
    const response = await api.get<Session[] | ApiEnvelope<Session[]>>(
      "/api/keylogger/sessions",
    );
    return unwrap<Session[]>(response);
  },
};
