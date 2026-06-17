import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Search } from 'lucide-react';
import { useDemo } from '../lib/demo-store';
import { AppShell } from '../components/Layout';
import { PostCard } from '../components/PostCard';

const TRENDING = ['ORR traffic', 'Metro', 'BBMP', 'Startup', 'Rain alert', 'Dasara'];

export function SearchPage() {
  const { searchPosts } = useDemo();
  const [q, setQ] = useState('');
  const results = q.length >= 2 ? searchPosts(q) : [];

  return (
    <AppShell title="Search">
      <div className="px-4">
        <div className="relative mb-6">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-[#666]" size={18} />
          <input value={q} onChange={e => setQ(e.target.value)} placeholder="Search news, reporters, topics…"
            className="input pl-11" autoFocus />
        </div>

        {!q && (
          <div>
            <p className="mb-3 text-sm font-semibold text-[#a8a8a8]">Trending</p>
            <div className="flex flex-wrap gap-2">
              {TRENDING.map(t => (
                <button key={t} type="button" onClick={() => setQ(t)}
                  className="rounded-full bg-[#1a1a1a] px-4 py-2 text-sm hover:bg-[#262626]">#{t}</button>
              ))}
            </div>
            <Link to="/track" className="card mt-6 block p-4">
              <p className="font-semibold">Track Investigation (IR)</p>
              <p className="mt-1 text-sm text-[#a8a8a8]">Look up IR-BLR-2026-00001 and more</p>
            </Link>
          </div>
        )}

        {q.length >= 2 && (
          <div className="space-y-4">
            <p className="text-sm text-[#a8a8a8]">{results.length} results for "{q}"</p>
            {results.map(p => <PostCard key={p.id} post={p} />)}
            {results.length === 0 && <p className="py-12 text-center text-[#a8a8a8]">No results found</p>}
          </div>
        )}
      </div>
    </AppShell>
  );
}
