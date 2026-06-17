import { Link } from 'react-router-dom';
import { BadgeCheck, LogOut, Settings, TrendingUp, Grid3X3 } from 'lucide-react';
import { useAuth } from '../lib/auth';
import { useDemo } from '../lib/demo-store';
import { AppShell } from '../components/Layout';
import { ReporterIdCard } from '../components/ReporterIdCard';
import { EARNINGS_SERIES } from '../mock/data';

export function ProfilePage() {
  const { user, logout } = useAuth();
  const { posts } = useDemo();

  if (!user) {
    return (
      <AppShell title="Profile">
        <div className="px-4 py-16 text-center">
          <p className="text-[#a8a8a8]"><Link to="/login" className="font-semibold text-sky-400">Log in</Link> to view your profile</p>
          <Link to="/" className="mt-4 inline-block text-sm text-[#666]">Browse as guest →</Link>
        </div>
      </AppShell>
    );
  }

  const userPosts = posts.filter(p => p.authorId === user.id && p.status === 'Published' && p.type !== 'Reel');
  const maxE = Math.max(...EARNINGS_SERIES.map(e => e.amount));

  return (
    <AppShell title="Profile">
      <div className="px-4">
        <div className="flex items-start gap-5 py-4">
          <img src={user.avatarUrl ?? `https://i.pravatar.cc/150?u=${user.id}`} alt="" className="h-20 w-20 rounded-full border-2 border-[#333] object-cover" />
          <div className="flex-1">
            <h2 className="flex items-center gap-2 text-lg font-bold">
              {user.displayName}
              {user.isPremium && <BadgeCheck className="text-sky-400" size={18} />}
            </h2>
            <p className="text-sm text-[#a8a8a8]">{user.email}</p>
            <p className="mt-1 rounded-full bg-[#262626] px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-[#a8a8a8] inline-block">{user.role}</p>
          </div>
          <button type="button" className="text-[#a8a8a8]"><Settings size={20} /></button>
        </div>

        <div className="mb-6 grid grid-cols-3 gap-3 text-center">
          <div><p className="text-lg font-bold">{userPosts.length || user.postsCount}</p><p className="text-xs text-[#a8a8a8]">Posts</p></div>
          <div><p className="text-lg font-bold">{user.followers.toLocaleString()}</p><p className="text-xs text-[#a8a8a8]">Followers</p></div>
          <div><p className="text-lg font-bold">{user.following}</p><p className="text-xs text-[#a8a8a8]">Following</p></div>
        </div>

        {(user.isPremium || user.role === 'Reporter') && (
          <div className="card mb-4 p-4">
            <div className="flex items-center justify-between">
              <p className="flex items-center gap-2 text-sm font-semibold"><TrendingUp size={16} className="text-green-400" /> Earnings dashboard</p>
              <p className="text-lg font-bold text-green-400">₹{user.earnings.toLocaleString()}</p>
            </div>
            <div className="mt-3 flex h-16 items-end gap-1">
              {EARNINGS_SERIES.map(e => (
                <div key={e.day} className="flex-1 rounded-t bg-gradient-to-t from-green-600/60 to-green-400/80" style={{ height: `${(e.amount / maxE) * 100}%`, minHeight: 3 }} />
              ))}
            </div>
            <p className="mt-2 text-[10px] text-[#666]">Demo analytics — last 7 days</p>
          </div>
        )}

        {user.reporterProfile?.status === 'Approved' && (
          <div className="mb-4"><ReporterIdCard user={user} /></div>
        )}

        {userPosts.length > 0 && (
          <div>
            <p className="mb-3 flex items-center gap-2 text-sm font-semibold"><Grid3X3 size={16} /> Posts</p>
            <div className="grid grid-cols-3 gap-0.5">
              {userPosts.map(p => {
                const m = p.media[0];
                return (
                  <Link key={p.id} to={`/post/${p.id}`} className="aspect-square overflow-hidden bg-[#1a1a1a]">
                    {m?.type === 'Image' && <img src={m.url} alt="" className="h-full w-full object-cover" />}
                    {m?.type === 'Video' && <img src={m.thumbnailUrl ?? m.url} alt="" className="h-full w-full object-cover" />}
                    {m?.type === 'Audio' && <div className="flex h-full items-center justify-center text-[#666] text-xs">Audio</div>}
                  </Link>
                );
              })}
            </div>
          </div>
        )}

        {['SuperAdmin', 'Admin', 'SubAdmin'].includes(user.role) && (
          <Link to="/admin" className="btn-primary mt-6 block text-center">Open admin panel</Link>
        )}

        <button type="button" onClick={logout} className="mt-4 flex w-full items-center justify-center gap-2 rounded-2xl border border-[#262626] py-3.5 text-sm text-red-400">
          <LogOut size={16} /> Log out
        </button>
      </div>
    </AppShell>
  );
}
