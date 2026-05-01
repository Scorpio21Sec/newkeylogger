'use client';

import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';

export interface AuthUser {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'viewer';
}

export interface AuthStore {
  token: string | null;
  user: AuthUser | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setToken: (token: string) => void;
  setUser: (user: AuthUser) => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        // In production, call backend authentication endpoint
        // For now, this is a mock implementation
        if (email && password.length >= 6) {
          const mockToken = btoa(`${email}:${Date.now()}`);
          const mockUser: AuthUser = {
            id: Math.random().toString(36).substr(2, 9),
            email,
            name: email.split('@')[0],
            role: 'user',
          };

          set({
            token: mockToken,
            user: mockUser,
            isAuthenticated: true,
          });
        } else {
          throw new Error('Invalid email or password');
        }
      },

      logout: () => {
        set({
          token: null,
          user: null,
          isAuthenticated: false,
        });
      },

      setToken: (token: string) => {
        set({ token, isAuthenticated: !!token });
      },

      setUser: (user: AuthUser) => {
        set({ user });
      },
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => {
        if (typeof window !== 'undefined') {
          return localStorage;
        }
        // Fallback for SSR
        return {
          getItem: () => null,
          setItem: () => {},
          removeItem: () => {},
        };
      }),
    }
  )
);

// Decode JWT token (for demonstration)
export function decodeToken(token: string): { email: string; timestamp: number } | null {
  try {
    const decoded = atob(token);
    const [email, timestamp] = decoded.split(':');
    return { email, timestamp: parseInt(timestamp, 10) };
  } catch {
    return null;
  }
}

// Check if token is expired (24-hour validity for demo)
export function isTokenExpired(token: string): boolean {
  const decoded = decodeToken(token);
  if (!decoded) return true;
  const now = Date.now();
  const tokenAge = now - decoded.timestamp;
  const expiryTime = 24 * 60 * 60 * 1000; // 24 hours
  return tokenAge > expiryTime;
}
