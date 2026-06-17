import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Users, FileCheck, Megaphone, Search, BarChart3, RefreshCw } from 'lucide-react';
import { useAuth } from '../lib/auth';
import { useDemo, resetDemo } from '../lib/demo-store';
import { AppShell } from '../components/Layout';
import { EARNINGS_SERIES } from '../mock/data';
import type { User } from '../types';

const TABS = [
  { id: 'overview', label: 'Overview', icon: BarChart3 },
  { id: 'reporters', label: 'Reporters', icon: Users },
  { id: 'posts', label: 'Posts', icon: FileCheck },
  { id: 'ads', label: 'Ads', icon: Megaphone },
  { id: 'ir', label: 'IR / Teams', icon: Search },
] as const;

const ROLES: User['role'][] = ['SuperAdmin', 'Admin', 'SubAdmin'];

export function AdminPage() {
  const { user } = useAuth();
  const demo = useDemo();
  const [tab, setTab] = useState<typeof TABS[number]['id']>('overview');
  const [irTitle, setIrTitle] = useState('');
  const [irDesc, setIrDesc] = useState('');
  const [newIr, setNewIr] = useState('');
  const [adTitle, setAdTitle] = useState('');

  const isAdmin = user && ROLES.includes(user.role);
  const stats = demo.getStats();
  const maxEarning = Math.max(...EARNINGS_SERIES.map(e => e.amount));

  if (!user) {
    return <AppShell title="Admin"><div className="px-4 py-12 text-center"><Link to="/login" className="text-sky-400">Log in</Link></div></AppShell>;
  }
  if (!isAdmin) {
    return <AppShell title="Admin"><div className="px-4 py-12 text-center text-red-400">Admin access required. Log in as admin@pressbangalore.demo</div></AppShell>;
  }

  const canManageIr = user.role !== 'SubAdmin';
  const canViewEarnings = user.role === 'SuperAdmin' || user.role === 'Admin';

  return (
    <AppShell title={`Admin · ${user.role}`}>
      <div className="px-4">
        {user.role === 'SuperAdmin' && (
          <div className="mb-4 card p-3">
            <p className="mb-2 text-xs text-[#a8a8a8]">Preview role (demo)</p>
            <div className="flex flex-wrap gap-2">
              {ROLES.map(r => (
                <button key={r} type="button" onClick={() => demo.switchRole(r)}
                  className={`chip ${user.role === r ? 'chip-active' : 'chip-inactive'}`}>{r}</button>
              ))}
            </div>
          </div>
        )}

        <div className="mb-4 flex gap-1 overflow-x-auto pb-1">
          {TABS.filter(t => (t.id === 'ir' ? canManageIr : t.id === 'ads' ? user.role !== 'SubAdmin' : true)).map(t => (
            <button key={t.id} type="button" onClick={() => setTab(t.id)}
              className={`flex shrink-0 items-center gap-1.5 rounded-full px-3 py-2 text-xs font-semibold ${tab === t.id ? 'bg-white text-black' : 'bg-[#262626]'}`}>
              <t.icon size={14} /> {t.label}
            </button>
          ))}
        </div>

        {tab === 'overview' && (
          <>
            <div className="mb-4 grid grid-cols-2 gap-3">
              {[
                ['Users', stats.totalUsers],
                ['Pending reporters', stats.pendingReporters],
                ['Pending posts', stats.pendingPosts],
                ['Open IRs', stats.openInvestigations],
              ].map(([l, v]) => (
                <div key={l as string} className="card p-4">
                  <p className="text-xs text-[#a8a8a8]">{l}</p>
                  <p className="text-2xl font-bold">{v}</p>
                </div>
              ))}
            </div>
            {canViewEarnings && (
              <div className="card mb-4 p-4">
                <p className="mb-3 text-sm font-semibold">Platform earnings (demo)</p>
                <div className="flex h-28 items-end gap-2">
                  {EARNINGS_SERIES.map(e => (
                    <div key={e.day} className="flex flex-1 flex-col items-center gap-1">
                      <div className="w-full rounded-t bg-gradient-to-t from-[#dd2a7b] to-[#f58529]" style={{ height: `${(e.amount / maxEarning) * 100}%`, minHeight: 4 }} />
                      <span className="text-[10px] text-[#666]">{e.day}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            <button type="button" onClick={resetDemo} className="btn-ghost flex w-full items-center justify-center gap-2 text-[#a8a8a8]">
              <RefreshCw size={14} /> Reset demo data
            </button>
          </>
        )}

        {tab === 'reporters' && (
          <div className="space-y-3">
            {demo.getPendingReporters().map(r => (
              <div key={r.id} className="card p-4">
                <p className="font-semibold">{r.user.displayName}</p>
                <p className="text-xs text-[#a8a8a8]">{r.user.email} · {r.area} · {r.beat}</p>
                <div className="mt-3 flex gap-2">
                  <button type="button" onClick={() => demo.approveReporter(r.id)} className="btn-primary flex-1 py-2 text-xs">Approve</button>
                  <button type="button" onClick={() => demo.rejectReporter(r.id, 'Incomplete documents')} className="btn-ghost flex-1 py-2 text-xs text-red-400">Reject</button>
                </div>
              </div>
            ))}
            {demo.getPendingReporters().length === 0 && <p className="py-8 text-center text-[#a8a8a8]">No pending reporters</p>}
          </div>
        )}

        {tab === 'posts' && (
          <div className="space-y-3">
            {demo.getPendingPosts().map(p => (
              <div key={p.id} className="card p-4">
                <p className="font-semibold">{p.title}</p>
                <p className="text-xs text-[#a8a8a8]">by {p.author.displayName} · {p.type}</p>
                <p className="mt-2 line-clamp-2 text-sm text-[#d4d4d4]">{p.body}</p>
                <div className="mt-3 flex gap-2">
                  <button type="button" onClick={() => demo.approvePost(p.id)} className="btn-primary flex-1 py-2 text-xs">Publish</button>
                  <button type="button" onClick={() => demo.rejectPost(p.id, 'Policy')} className="btn-ghost flex-1 py-2 text-xs">Reject</button>
                </div>
              </div>
            ))}
            {demo.getPendingPosts().length === 0 && <p className="py-8 text-center text-[#a8a8a8]">No pending posts</p>}
          </div>
        )}

        {tab === 'ads' && canManageIr && (
          <div className="space-y-4">
            <form onSubmit={e => {
              e.preventDefault();
              demo.createAd({ title: adTitle, imageUrl: `https://picsum.photos/seed/${Date.now()}/800/280`, linkUrl: '#', slot: 'FeedInline', targetCity: 'Bangalore' });
              setAdTitle('');
            }} className="card space-y-3 p-4">
              <p className="font-semibold">New advertisement</p>
              <input value={adTitle} onChange={e => setAdTitle(e.target.value)} placeholder="Ad title" className="input" required />
              <button type="submit" className="btn-primary w-full py-2 text-sm">Create ad</button>
            </form>
            {demo.ads.map(ad => (
              <div key={ad.id} className="card overflow-hidden">
                <img src={ad.imageUrl} alt="" className="h-24 w-full object-cover" />
                <div className="flex items-center justify-between p-3">
                  <div>
                    <p className="text-sm font-medium">{ad.title}</p>
                    <p className="text-xs text-[#a8a8a8]">{ad.slot} · {ad.isActive ? 'Active' : 'Paused'}</p>
                  </div>
                  <button type="button" onClick={() => demo.toggleAd(ad.id)} className="btn-ghost py-1 text-xs">
                    {ad.isActive ? 'Pause' : 'Activate'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {tab === 'ir' && canManageIr && (
          <div className="space-y-4">
            <form onSubmit={e => {
              e.preventDefault();
              const ir = demo.createInvestigation(irTitle, irDesc);
              setNewIr(ir.irNumber);
              setIrTitle(''); setIrDesc('');
            }} className="card space-y-3 p-4">
              <p className="font-semibold">Create investigation (IR)</p>
              <input value={irTitle} onChange={e => setIrTitle(e.target.value)} placeholder="Title" className="input" required />
              <textarea value={irDesc} onChange={e => setIrDesc(e.target.value)} placeholder="Description" className="input" rows={2} required />
              <button type="submit" className="btn-primary w-full py-2 text-sm">Generate IR number</button>
              {newIr && <p className="text-center font-mono text-sm text-green-400">Created: {newIr}</p>}
            </form>

            {demo.investigations.map(ir => (
              <div key={ir.id} className="card p-4">
                <p className="font-mono text-sm text-sky-400">{ir.irNumber}</p>
                <p className="font-semibold">{ir.title}</p>
                <p className="mt-1 text-xs text-[#a8a8a8]">{ir.status} {ir.ioName ? `· IO: ${ir.ioName}` : ''}</p>
                {ir.assignments.length > 0 && (
                  <p className="mt-2 text-xs">Teams: {ir.assignments.map(a => a.teamName).join(', ')}</p>
                )}
                {ir.reports.length > 0 && (
                  <div className="mt-2 rounded-lg bg-[#1a1a1a] p-2 text-xs">
                    <p className="font-semibold text-[#a8a8a8]">Consolidated reports</p>
                    {ir.reports.map((r, i) => <p key={i} className="mt-1">{r.teamName}: {r.reportBody.slice(0, 80)}…</p>)}
                  </div>
                )}
                {!ir.ioUserId && (
                  <button type="button" onClick={() => demo.assignIo(ir.id, 'u-ops')} className="btn-ghost mt-2 w-full py-1.5 text-xs">Assign IO</button>
                )}
                {ir.ioUserId && ir.assignments.length === 0 && (
                  <button type="button" onClick={() => demo.assignTeam(ir.id, 't1')} className="btn-ghost mt-2 w-full py-1.5 text-xs">Assign Team Alpha</button>
                )}
              </div>
            ))}

            <div className="card p-4">
              <p className="mb-2 font-semibold">Teams</p>
              {demo.teams.map(t => (
                <div key={t.id} className="mb-2 text-sm">
                  <p className="font-medium">{t.name} <span className="text-[#a8a8a8]">({t.region})</span></p>
                  <p className="text-xs text-[#666]">{t.members.join(' · ')}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
