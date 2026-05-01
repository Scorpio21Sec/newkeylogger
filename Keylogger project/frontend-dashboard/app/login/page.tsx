'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useAuthStore } from '@/store/auth-store';
import { Card } from '@/components/ui/card';
import { Sparkles } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuthStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      router.push('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 px-4">
      {/* Background blur effect */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -left-40 -top-40 h-80 w-80 rounded-full bg-cyan-500/20 blur-3xl" />
        <div className="absolute -right-40 -bottom-40 h-80 w-80 rounded-full bg-blue-500/20 blur-3xl" />
      </div>

      <Card className="relative w-full max-w-md border border-slate-700/50 bg-slate-900/80 backdrop-blur">
        <div className="space-y-6 p-8">
          {/* Header */}
          <div className="space-y-2 text-center">
            <div className="inline-flex items-center gap-2 rounded-full bg-cyan-400/15 px-3 py-1 text-sm text-cyan-200 ring-1 ring-cyan-300/30">
              <Sparkles size={16} />
              Analytics Dashboard
            </div>
            <h1 className="text-2xl font-bold text-white">Welcome Back</h1>
            <p className="text-sm text-slate-400">Sign in to access your typing analytics</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="rounded-lg bg-red-500/10 p-3 text-sm text-red-200 ring-1 ring-red-500/20">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="email" className="mb-2 block text-sm font-medium text-slate-300">
                Email Address
              </label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading}
                className="w-full"
              />
            </div>

            <div>
              <label htmlFor="password" className="mb-2 block text-sm font-medium text-slate-300">
                Password
              </label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
                className="w-full"
              />
              <p className="mt-1 text-xs text-slate-500">Minimum 6 characters</p>
            </div>

            <Button
              type="submit"
              disabled={loading || !email || password.length < 6}
              className="w-full"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>

          {/* Demo credentials */}
          <div className="rounded-lg bg-blue-500/10 p-3 text-xs text-blue-200 ring-1 ring-blue-500/20">
            <p className="font-medium mb-1">Demo Credentials:</p>
            <p>Email: demo@example.com</p>
            <p>Password: password123</p>
          </div>

          {/* Footer */}
          <p className="text-center text-xs text-slate-500">
            This is a demo environment. No real authentication required.
          </p>
        </div>
      </Card>
    </div>
  );
}
