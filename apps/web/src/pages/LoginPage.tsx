import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/auth';
import { DEMO_PASSWORD } from '../mock/data';
import { BackButton } from '../components/BackButton';

const ACCOUNTS = [
  { email: 'admin@pressbangalore.demo', label: 'Super Admin' },
  { email: 'reporter@pressbangalore.demo', label: 'Reporter (approved)' },
  { email: 'pending@pressbangalore.demo', label: 'Reporter (pending)' },
  { email: 'user@pressbangalore.demo', label: 'Premium user' },
];

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('admin@pressbangalore.demo');
  const [password, setPassword] = useState(DEMO_PASSWORD);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await login(email, password);
      navigate('/');
    } catch {
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col justify-center bg-black px-6">
      <div className="absolute left-2 top-safe pt-2">
        <BackButton />
      </div>
      <div className="mx-auto w-full max-w-sm">
        <div className="mb-10 text-center">
          <h1 className="gradient-text text-4xl font-bold">PressBangalore</h1>
          <p className="mt-2 text-sm text-[#a8a8a8]">Local news. Verified reporters. Your city.</p>
        </div>

        <form onSubmit={submit} className="space-y-3">
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" required className="input" />
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" required className="input" />
          {error && <p className="text-center text-sm text-red-400">{error}</p>}
          <button type="submit" disabled={loading} className="btn-primary w-full disabled:opacity-50">
            {loading ? 'Signing in…' : 'Log in'}
          </button>
        </form>

        <div className="mt-6">
          <p className="mb-2 text-center text-xs font-semibold uppercase tracking-wider text-[#666]">Quick demo login</p>
          <div className="flex flex-wrap justify-center gap-2">
            {ACCOUNTS.map(a => (
              <button key={a.email} type="button" onClick={() => setEmail(a.email)}
                className="rounded-full bg-[#1a1a1a] px-3 py-1.5 text-[11px] text-[#a8a8a8] hover:bg-[#262626]">{a.label}</button>
            ))}
          </div>
          <p className="mt-3 text-center text-[11px] text-[#666]">Password: {DEMO_PASSWORD}</p>
        </div>

        <p className="mt-8 text-center text-sm text-[#a8a8a8]">
          New here? <Link to="/register" className="font-semibold text-sky-400">Sign up</Link>
        </p>
        <p className="mt-4 text-center">
          <Link to="/" className="text-xs text-[#666]">Continue without login →</Link>
        </p>
      </div>
    </div>
  );
}
