import { useNavigate, useLocation } from 'react-router-dom';
import { Home, Clapperboard, PlusSquare, Search, User, Shield, Bell } from 'lucide-react';
import { useAuth } from '../lib/auth';

export function BottomNav() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const isAdmin = user && ['SuperAdmin', 'Admin', 'SubAdmin'].includes(user.role);

  const tabs = [
    { to: '/', label: 'Home', icon: Home, end: true },
    { to: '/reels', label: 'Reels', icon: Clapperboard },
    { to: '/reporter', label: 'Create', icon: PlusSquare },
    { to: '/search', label: 'Search', icon: Search },
    isAdmin
      ? { to: '/admin', label: 'Admin', icon: Shield }
      : { to: '/profile', label: 'Profile', icon: User },
  ] as const;

  const goTab = (to: string) => {
    if (location.pathname !== to) {
      navigate(to);
    }
  };

  const linkClass = (active: boolean) =>
    `flex flex-col items-center gap-0.5 transition ${active ? 'text-white scale-105' : 'text-[#a8a8a8]'}`;

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-[#262626]/80 bg-black/95 backdrop-blur-xl safe-bottom">
      <div className="mx-auto flex max-w-lg items-center justify-around px-1 py-2">
        {tabs.map(tab => {
          const active = 'end' in tab && tab.end ? location.pathname === tab.to : location.pathname.startsWith(tab.to);
          const Icon = tab.icon;
          return (
            <button
              key={tab.to}
              type="button"
              onClick={() => goTab(tab.to)}
              className={linkClass(active)}
            >
              <Icon size={26} strokeWidth={1.8} />
              <span className="text-[10px]">{tab.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}

export function AppShell({ children, title, showHeader = true }: { children: React.ReactNode; title?: string; showHeader?: boolean }) {
  return (
    <div className="min-h-full pb-[72px]">
      {showHeader && (
        <header className="sticky top-0 z-40 border-b border-[#262626]/80 bg-black/90 backdrop-blur-xl">
          <div className="mx-auto flex max-w-lg items-center justify-between px-4 py-3">
            <h1 className="gradient-text text-xl font-bold tracking-tight">PressBangalore</h1>
            <div className="flex items-center gap-3">
              {title && <span className="text-xs text-[#a8a8a8]">{title}</span>}
              <button type="button" className="relative text-white" aria-label="Notifications">
                <Bell size={22} strokeWidth={1.8} />
                <span className="absolute -right-0.5 -top-0.5 h-2 w-2 rounded-full bg-[#dd2a7b]" />
              </button>
            </div>
          </div>
        </header>
      )}
      <main className="mx-auto max-w-lg">{children}</main>
      <BottomNav />
    </div>
  );
}
