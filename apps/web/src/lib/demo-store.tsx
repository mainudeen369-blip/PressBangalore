import {
  createContext, useContext, useState, useCallback, useEffect, useMemo, type ReactNode,
} from 'react';
import {
  DEMO_PASSWORD, INITIAL_ADS, INITIAL_INVESTIGATIONS, INITIAL_POSTS, INITIAL_TEAMS, INITIAL_USERS,
  nextIrNumber,
} from '../mock/data';
import type {
  Advertisement, DashboardStats, Investigation, NewsPost, ReporterProfile, Team, User,
} from '../types';

const STORAGE_KEY = 'pb_demo_state_v1';

interface PersistedState {
  currentUserId: string | null;
  users: User[];
  posts: NewsPost[];
  ads: Advertisement[];
  investigations: Investigation[];
  teams: Team[];
  likedPosts: string[];
}

interface DemoStore extends PersistedState {
  currentUser: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (displayName: string, email: string, password: string) => Promise<void>;
  registerReporter: (input: { area: string; beat: string; languages: string; idDocumentUrl?: string }) => void;
  createPost: (input: {
    title: string; body: string; type: NewsPost['type']; language: string;
    mediaUrl: string; mediaType: 'Image' | 'Video' | 'Audio'; durationSec?: number;
  }) => void;
  approveReporter: (profileId: string) => void;
  rejectReporter: (profileId: string, reason: string) => void;
  approvePost: (postId: string) => void;
  rejectPost: (postId: string, reason: string) => void;
  createInvestigation: (title: string, description: string, cityCode?: string) => Investigation;
  assignIo: (irId: string, userId: string) => void;
  assignTeam: (irId: string, teamId: string) => void;
  createAd: (ad: Omit<Advertisement, 'id' | 'isActive'>) => void;
  toggleAd: (adId: string) => void;
  toggleLike: (postId: string) => void;
  isLiked: (postId: string) => boolean;
  switchRole: (role: User['role']) => void;
  getFeed: (city?: string, language?: string | null) => NewsPost[];
  getReels: () => NewsPost[];
  getPost: (id: string) => NewsPost | undefined;
  getPendingReporters: () => (ReporterProfile & { user: User })[];
  getPendingPosts: () => NewsPost[];
  getStats: () => DashboardStats;
  trackIr: (irNumber: string) => Investigation | undefined;
  searchPosts: (q: string) => NewsPost[];
}

function loadState(): PersistedState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw) as PersistedState;
  } catch { /* ignore */ }
  return {
    currentUserId: null,
    users: structuredClone(INITIAL_USERS),
    posts: structuredClone(INITIAL_POSTS),
    ads: structuredClone(INITIAL_ADS),
    investigations: structuredClone(INITIAL_INVESTIGATIONS),
    teams: structuredClone(INITIAL_TEAMS),
    likedPosts: [],
  };
}

function uid() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

const DemoContext = createContext<DemoStore | null>(null);

export function DemoProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<PersistedState>(loadState);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [state]);

  const currentUser = useMemo(
    () => state.users.find(u => u.id === state.currentUserId) ?? null,
    [state.users, state.currentUserId],
  );

  const update = useCallback((fn: (s: PersistedState) => PersistedState) => {
    setState(prev => fn(prev));
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    await new Promise(r => setTimeout(r, 400));
    const user = state.users.find(u => u.email.toLowerCase() === email.toLowerCase());
    if (!user || password !== DEMO_PASSWORD) {
      setLoading(false);
      throw new Error('Invalid credentials');
    }
    const fresh = state.users.find(u => u.id === user.id) ?? user;
    update(s => ({ ...s, currentUserId: fresh.id }));
    setLoading(false);
  };

  const logout = () => update(s => ({ ...s, currentUserId: null }));

  const register = async (displayName: string, email: string, _password: string) => {
    await new Promise(r => setTimeout(r, 400));
    const newUser: User = {
      id: `u-${uid()}`,
      email: email.toLowerCase(),
      displayName,
      avatarUrl: `https://i.pravatar.cc/150?u=${encodeURIComponent(email)}`,
      role: 'Consumer',
      isPremium: false,
      languagePref: 'en',
      city: 'Bangalore',
      followers: 0,
      following: 0,
      earnings: 0,
      postsCount: 0,
    };
    update(s => ({ ...s, users: [...s.users, newUser], currentUserId: newUser.id }));
  };

  const registerReporter = (input: { area: string; beat: string; languages: string; idDocumentUrl?: string }) => {
    if (!currentUser) return;
    const profile: ReporterProfile = {
      id: `rp-${uid()}`,
      area: input.area,
      beat: input.beat,
      languages: input.languages,
      status: 'Pending',
      idDocumentUrl: input.idDocumentUrl ?? 'https://picsum.photos/seed/upload/400/250',
    };
    update(s => ({
      ...s,
      users: s.users.map(u => u.id === currentUser.id
        ? { ...u, role: 'Reporter' as const, reporterProfile: profile }
        : u),
    }));
  };

  const createPost = (input: {
    title: string; body: string; type: NewsPost['type']; language: string;
    mediaUrl: string; mediaType: 'Image' | 'Video' | 'Audio'; durationSec?: number;
  }) => {
    if (!currentUser) return;
    const isAdmin = ['SuperAdmin', 'Admin', 'SubAdmin'].includes(currentUser.role);
    const approved = currentUser.reporterProfile?.status === 'Approved';
    if (!isAdmin && !approved) return;

    const post: NewsPost = {
      id: `p-${uid()}`,
      authorId: currentUser.id,
      title: input.title,
      body: input.body,
      type: input.type,
      status: isAdmin ? 'Published' : 'PendingApproval',
      city: currentUser.city,
      language: input.language,
      likesCount: 0,
      viewsCount: 0,
      durationSec: input.durationSec,
      createdAt: new Date().toISOString(),
      author: {
        id: currentUser.id,
        displayName: currentUser.displayName,
        avatarUrl: currentUser.avatarUrl,
        isPremium: currentUser.isPremium,
      },
      media: [{ id: `m-${uid()}`, type: input.mediaType, url: input.mediaUrl }],
    };
    update(s => ({ ...s, posts: [post, ...s.posts] }));
  };

  const approveReporter = (profileId: string) => {
    update(s => ({
      ...s,
      users: s.users.map(u => u.reporterProfile?.id === profileId
        ? {
          ...u,
          reporterProfile: {
            ...u.reporterProfile!,
            status: 'Approved' as const,
            pressId: `PB-REP-2026-${String(Math.floor(Math.random() * 9000) + 1000)}`,
            appointedDate: new Date().toISOString().slice(0, 10),
            appointmentLetterUrl: 'https://picsum.photos/seed/letter-new/400/560',
          },
        }
        : u),
    }));
  };

  const rejectReporter = (profileId: string, reason: string) => {
    update(s => ({
      ...s,
      users: s.users.map(u => u.reporterProfile?.id === profileId
        ? { ...u, reporterProfile: { ...u.reporterProfile!, status: 'Rejected' as const, rejectionReason: reason } }
        : u),
    }));
  };

  const approvePost = (postId: string) => {
    update(s => ({
      ...s,
      posts: s.posts.map(p => p.id === postId ? { ...p, status: 'Published' as const } : p),
    }));
  };

  const rejectPost = (postId: string, _reason: string) => {
    update(s => ({
      ...s,
      posts: s.posts.map(p => p.id === postId ? { ...p, status: 'Rejected' as const } : p),
    }));
  };

  const createInvestigation = (title: string, description: string, cityCode = 'BLR') => {
    const ir: Investigation = {
      id: `ir-${uid()}`,
      irNumber: nextIrNumber(cityCode, state.investigations),
      title,
      description,
      status: 'Open',
      createdAt: new Date().toISOString(),
      assignments: [],
      reports: [],
    };
    update(s => ({ ...s, investigations: [ir, ...s.investigations] }));
    return ir;
  };

  const assignIo = (irId: string, userId: string) => {
    const io = state.users.find(u => u.id === userId);
    update(s => ({
      ...s,
      investigations: s.investigations.map(ir => ir.id === irId
        ? { ...ir, ioUserId: userId, ioName: io?.displayName, status: 'Assigned' as const }
        : ir),
    }));
  };

  const assignTeam = (irId: string, teamId: string) => {
    const team = state.teams.find(t => t.id === teamId);
    if (!team) return;
    update(s => ({
      ...s,
      investigations: s.investigations.map(ir => {
        if (ir.id !== irId) return ir;
        const hasTeam = ir.assignments.some(a => a.teamId === teamId);
        return {
          ...ir,
          status: ir.status === 'Assigned' ? 'InProgress' as const : ir.status,
          assignments: hasTeam ? ir.assignments : [...ir.assignments, { teamId, teamName: team.name, role: 'Member' }],
        };
      }),
    }));
  };

  const createAd = (ad: Omit<Advertisement, 'id' | 'isActive'>) => {
    update(s => ({
      ...s,
      ads: [{ ...ad, id: `ad-${uid()}`, isActive: true }, ...s.ads],
    }));
  };

  const toggleAd = (adId: string) => {
    update(s => ({
      ...s,
      ads: s.ads.map(a => a.id === adId ? { ...a, isActive: !a.isActive } : a),
    }));
  };

  const toggleLike = (postId: string) => {
    update(s => {
      const liked = s.likedPosts.includes(postId);
      return {
        ...s,
        likedPosts: liked ? s.likedPosts.filter(id => id !== postId) : [...s.likedPosts, postId],
        posts: s.posts.map(p => p.id === postId
          ? { ...p, likesCount: p.likesCount + (liked ? -1 : 1) }
          : p),
      };
    });
  };

  const isLiked = (postId: string) => state.likedPosts.includes(postId);

  const switchRole = (role: User['role']) => {
    if (!currentUser) return;
    update(s => ({
      ...s,
      users: s.users.map(u => u.id === currentUser.id ? { ...u, role } : u),
    }));
  };

  const getFeed = (city?: string, language?: string | null) =>
    state.posts.filter(p =>
      p.status === 'Published' && p.type !== 'Reel'
      && (!city || p.city === city)
      && (!language || p.language === language),
    );

  const getReels = () => state.posts.filter(p => p.status === 'Published' && p.type === 'Reel');

  const getPost = (id: string) => state.posts.find(p => p.id === id);

  const getPendingReporters = () =>
    state.users
      .filter(u => u.reporterProfile?.status === 'Pending')
      .map(u => ({ ...u.reporterProfile!, user: u }));

  const getPendingPosts = () => state.posts.filter(p => p.status === 'PendingApproval');

  const getStats = (): DashboardStats => ({
    totalUsers: state.users.length,
    pendingReporters: state.users.filter(u => u.reporterProfile?.status === 'Pending').length,
    pendingPosts: state.posts.filter(p => p.status === 'PendingApproval').length,
    publishedPosts: state.posts.filter(p => p.status === 'Published').length,
    openInvestigations: state.investigations.filter(i => i.status !== 'Closed').length,
  });

  const trackIr = (irNumber: string) =>
    state.investigations.find(i => i.irNumber.toUpperCase() === irNumber.toUpperCase());

  const searchPosts = (q: string) => {
    const lower = q.toLowerCase();
    return state.posts.filter(p =>
      p.status === 'Published' && (
        p.title.toLowerCase().includes(lower)
        || p.body.toLowerCase().includes(lower)
        || p.author.displayName.toLowerCase().includes(lower)
      ),
    );
  };

  const value: DemoStore = {
    ...state,
    currentUser,
    loading,
    login,
    logout,
    register,
    registerReporter,
    createPost,
    approveReporter,
    rejectReporter,
    approvePost,
    rejectPost,
    createInvestigation,
    assignIo,
    assignTeam,
    createAd,
    toggleAd,
    toggleLike,
    isLiked,
    switchRole,
    getFeed,
    getReels,
    getPost,
    getPendingReporters,
    getPendingPosts,
    getStats,
    trackIr,
    searchPosts,
  };

  return <DemoContext.Provider value={value}>{children}</DemoContext.Provider>;
}

export function useDemo() {
  const ctx = useContext(DemoContext);
  if (!ctx) throw new Error('useDemo must be used within DemoProvider');
  return ctx;
}

export function resetDemo() {
  localStorage.removeItem(STORAGE_KEY);
  window.location.reload();
}
