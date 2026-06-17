import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDemo } from '../lib/demo-store';
import { BackButton } from '../components/BackButton';

export function RegisterPage() {
  const { register } = useDemo();
  const navigate = useNavigate();
  const [displayName, setDisplayName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register(displayName, email, password);
      navigate('/');
    } catch {
      setError('Registration failed');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-black px-6">
      <div className="absolute left-2 top-safe pt-2">
        <BackButton />
      </div>
      <div className="w-full max-w-sm">
        <h1 className="mb-2 text-2xl font-bold">Create account</h1>
        <p className="mb-8 text-sm text-[#a8a8a8]">Join PressBangalore — demo mode, no backend required.</p>
        <form onSubmit={submit} className="space-y-3">
          <input value={displayName} onChange={e => setDisplayName(e.target.value)} placeholder="Display name" required className="input" />
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" required className="input" />
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" required className="input" />
          {error && <p className="text-sm text-red-400">{error}</p>}
          <button type="submit" className="btn-primary w-full">Sign up</button>
        </form>
        <p className="mt-6 text-center text-sm text-[#a8a8a8]">
          Have an account? <Link to="/login" className="text-sky-400">Log in</Link>
        </p>
      </div>
    </div>
  );
}
