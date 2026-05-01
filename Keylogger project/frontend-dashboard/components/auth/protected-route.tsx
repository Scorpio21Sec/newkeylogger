'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore, isTokenExpired } from '@/store/auth-store';
import { DashboardLoading } from '@/components/dashboard/dashboard-loading';

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { token, isAuthenticated } = useAuthStore();

  useEffect(() => {
    // Check if user is authenticated and token is not expired
    if (!isAuthenticated || !token || isTokenExpired(token)) {
      router.push('/login');
    }
  }, [isAuthenticated, token, router]);

  if (!isAuthenticated || !token) {
    return <DashboardLoading />;
  }

  return <>{children}</>;
}
