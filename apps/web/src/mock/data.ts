import type {
  Advertisement, Investigation, NewsPost, Team, User,
} from '../types';

export const DEMO_PASSWORD = 'Demo@123';

export const CITIES = ['Bangalore', 'Mysuru', 'Mangalore', 'Hubballi'] as const;
export const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'kn', label: 'ಕನ್ನಡ' },
  { code: 'hi', label: 'हिंदी' },
] as const;

export const STORIES = [
  { id: 's1', name: 'Ravi K.', avatar: 'https://i.pravatar.cc/150?u=ravi', hasNew: true },
  { id: 's2', name: 'Priya N.', avatar: 'https://i.pravatar.cc/150?u=priya', hasNew: true },
  { id: 's3', name: 'City Beat', avatar: 'https://i.pravatar.cc/150?u=city', hasNew: true },
  { id: 's4', name: 'Kannada', avatar: 'https://i.pravatar.cc/150?u=kn', hasNew: false },
  { id: 's5', name: 'Sports', avatar: 'https://i.pravatar.cc/150?u=sport', hasNew: true },
  { id: 's6', name: 'Business', avatar: 'https://i.pravatar.cc/150?u=biz', hasNew: false },
];

const sampleVideo = 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4';
const sampleVideo2 = 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4';
const sampleAudio = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3';

export const INITIAL_USERS: User[] = [
  {
    id: 'u-admin',
    email: 'admin@pressbangalore.demo',
    displayName: 'Super Admin',
    avatarUrl: 'https://i.pravatar.cc/150?u=admin',
    role: 'SuperAdmin',
    isPremium: true,
    languagePref: 'en',
    city: 'Bangalore',
    followers: 0,
    following: 0,
    earnings: 24800,
    postsCount: 0,
  },
  {
    id: 'u-ops',
    email: 'ops@pressbangalore.demo',
    displayName: 'Ops Admin',
    avatarUrl: 'https://i.pravatar.cc/150?u=ops',
    role: 'Admin',
    isPremium: true,
    languagePref: 'en',
    city: 'Bangalore',
    followers: 120,
    following: 45,
    earnings: 12400,
    postsCount: 2,
  },
  {
    id: 'u-mod',
    email: 'moderator@pressbangalore.demo',
    displayName: 'Sub Admin',
    avatarUrl: 'https://i.pravatar.cc/150?u=mod',
    role: 'SubAdmin',
    isPremium: false,
    languagePref: 'en',
    city: 'Bangalore',
    followers: 80,
    following: 30,
    earnings: 0,
    postsCount: 0,
  },
  {
    id: 'u-reporter',
    email: 'reporter@pressbangalore.demo',
    displayName: 'Ravi Kumar',
    avatarUrl: 'https://i.pravatar.cc/150?u=reporter',
    role: 'Reporter',
    isPremium: false,
    languagePref: 'kn',
    city: 'Bangalore',
    followers: 4200,
    following: 180,
    earnings: 8600,
    postsCount: 24,
    reporterProfile: {
      id: 'rp-1',
      area: 'Koramangala',
      beat: 'South Bangalore',
      languages: 'en,kn',
      status: 'Approved',
      idDocumentUrl: 'https://picsum.photos/seed/idcard/400/250',
      appointmentLetterUrl: 'https://picsum.photos/seed/letter/400/560',
      appointedDate: '2025-11-01',
      pressId: 'PB-REP-2025-0042',
    },
  },
  {
    id: 'u-pending',
    email: 'pending@pressbangalore.demo',
    displayName: 'Anitha S',
    avatarUrl: 'https://i.pravatar.cc/150?u=anitha',
    role: 'Reporter',
    isPremium: false,
    languagePref: 'en',
    city: 'Bangalore',
    followers: 120,
    following: 90,
    earnings: 0,
    postsCount: 0,
    reporterProfile: {
      id: 'rp-2',
      area: 'Whitefield',
      beat: 'East Bangalore',
      languages: 'en',
      status: 'Pending',
      idDocumentUrl: 'https://picsum.photos/seed/id2/400/250',
    },
  },
  {
    id: 'u-premium',
    email: 'user@pressbangalore.demo',
    displayName: 'Priya N',
    avatarUrl: 'https://i.pravatar.cc/150?u=priya2',
    role: 'Premium',
    isPremium: true,
    languagePref: 'en',
    city: 'Bangalore',
    followers: 1280,
    following: 340,
    earnings: 3200,
    postsCount: 8,
  },
  {
    id: 'u-consumer',
    email: 'guest@pressbangalore.demo',
    displayName: 'Arjun M',
    avatarUrl: 'https://i.pravatar.cc/150?u=arjun',
    role: 'Consumer',
    isPremium: false,
    languagePref: 'kn',
    city: 'Mysuru',
    followers: 45,
    following: 120,
    earnings: 0,
    postsCount: 0,
  },
];

export const INITIAL_POSTS: NewsPost[] = [
  post('p1', 'u-reporter', 'Traffic advisory on ORR', 'Heavy congestion reported near Silk Board junction. Commuters advised to use alternate routes via HSR Layout.', 'News', 'Published', 'Bangalore', 'en', 'https://picsum.photos/seed/pb1/800/600', 'image'),
  post('p2', 'u-reporter', 'ಬೆಳ್ಳಂದೂರು ಕೆರೆ ಪುನರ್‌ಸ್ಥಾಪನೆ', 'BBMP begins lake restoration work this week with citizen oversight committee.', 'News', 'Published', 'Bangalore', 'kn', 'https://picsum.photos/seed/pb2/800/600', 'image'),
  post('p3', 'u-reporter', 'Startup funding roundup', 'Three Bangalore startups raised Series A this month — fintech, healthtech, and agritech lead the charts.', 'Business', 'Published', 'Bangalore', 'en', 'https://picsum.photos/seed/pb3/800/600', 'image'),
  post('p4', 'u-reporter', 'Weekend food fest in Indiranagar', 'Best street food spots and live music this Saturday. Entry free before 6 PM.', 'Entertainment', 'Published', 'Bangalore', 'en', 'https://picsum.photos/seed/pb4/800/600', 'image'),
  post('p5', 'u-reporter', 'Metro expansion update', 'Namma Metro Phase 3 progress — new stations opening Q3 2026.', 'Professional', 'Published', 'Bangalore', 'en', sampleVideo, 'video', 'https://picsum.photos/seed/reel1/400/700'),
  post('p6', 'u-reporter', 'ಮಳೆ ಎಚ್ಚರಿಕೆ', 'IMD issues yellow alert for Bangalore urban and rural districts.', 'News', 'Published', 'Bangalore', 'kn', sampleVideo2, 'video', 'https://picsum.photos/seed/reel2/400/700'),
  post('p7', 'u-reporter', 'Press briefing audio', 'Full audio from today\'s BBMP press conference on ward-wise development.', 'News', 'Published', 'Bangalore', 'en', sampleAudio, 'audio'),
  post('p8', 'u-pending', 'Whitefield infra probe', 'Residents report delayed road work near ITPL main road.', 'News', 'PendingApproval', 'Bangalore', 'en', 'https://picsum.photos/seed/pb8/800/600', 'image'),
  post('p9', 'u-reporter', 'Mysuru Dasara prep', 'City administration gears up for Dasara celebrations with enhanced security.', 'News', 'Published', 'Mysuru', 'kn', 'https://picsum.photos/seed/pb9/800/600', 'image'),
  post('p10', 'u-reporter', 'Coastal weather watch', 'Fishermen advised caution along Mangalore coast.', 'News', 'Published', 'Mangalore', 'kn', 'https://picsum.photos/seed/pb10/800/600', 'image'),
  post('r1', 'u-reporter', 'Silk Board in 15 sec', 'Quick traffic snapshot from ground zero.', 'Reel', 'Published', 'Bangalore', 'en', sampleVideo, 'video', 'https://picsum.photos/seed/r1/400/700', 15),
  post('r2', 'u-reporter', 'Street food reel', 'Must-try dishes this weekend!', 'Reel', 'Published', 'Bangalore', 'en', sampleVideo2, 'video', 'https://picsum.photos/seed/r2/400/700', 22),
  post('r3', 'u-premium', 'Morning yoga at Cubbon', 'Wellness Sunday series.', 'Reel', 'Published', 'Bangalore', 'en', sampleVideo, 'video', 'https://picsum.photos/seed/r3/400/700', 18),
  post('r4', 'u-reporter', 'ಕನ್ನಡ ಸಂಸ್ಕೃತಿ', 'Heritage walk highlights from old Bangalore.', 'Reel', 'Published', 'Bangalore', 'kn', sampleVideo2, 'video', 'https://picsum.photos/seed/r4/400/700', 30),
];

export const INITIAL_ADS: Advertisement[] = [
  { id: 'ad1', title: 'Bangalore Coffee Festival 2026', imageUrl: 'https://picsum.photos/seed/ad1/800/280', linkUrl: '#', slot: 'FeedTop', targetCity: 'Bangalore', isActive: true },
  { id: 'ad2', title: 'Local Business Spotlight — Koramangala', imageUrl: 'https://picsum.photos/seed/ad2/800/280', linkUrl: '#', slot: 'FeedInline', targetCity: 'Bangalore', isActive: true },
  { id: 'ad3', title: 'Premium subscription — 50% off', imageUrl: 'https://picsum.photos/seed/ad3/800/280', linkUrl: '#', slot: 'Reels', targetCity: null, isActive: true },
];

export const INITIAL_TEAMS: Team[] = [
  { id: 't1', name: 'Team Alpha', region: 'Bangalore South', members: ['Ravi Kumar', 'Suresh G', 'Meena K'] },
  { id: 't2', name: 'Team Beta', region: 'Bangalore East', members: ['Anitha S', 'Karthik R', 'Divya P'] },
  { id: 't3', name: 'Team Gamma', region: 'Mysuru', members: ['Rajesh M', 'Lakshmi S'] },
];

export const INITIAL_INVESTIGATIONS: Investigation[] = [
  {
    id: 'ir1',
    irNumber: 'IR-BLR-2026-00001',
    title: 'Land encroachment inquiry — Bellandur buffer zone',
    description: 'Investigation into reported encroachment near lake buffer zone following citizen complaints.',
    status: 'InProgress',
    ioName: 'Ops Admin',
    ioUserId: 'u-ops',
    createdAt: '2026-06-01T10:00:00Z',
    assignments: [{ teamId: 't1', teamName: 'Team Alpha', role: 'Lead' }],
    reports: [
      { teamName: 'Team Alpha', reportBody: 'Site survey completed. Preliminary findings suggest unauthorized structures on plot 42-B.', submittedAt: '2026-06-10T14:00:00Z' },
    ],
  },
  {
    id: 'ir2',
    irNumber: 'IR-BLR-2026-00002',
    title: 'Public works contract compliance review',
    description: 'Review of ORR road repair contract compliance and material quality audit.',
    status: 'Assigned',
    ioName: 'Sub Admin',
    ioUserId: 'u-mod',
    createdAt: '2026-06-08T09:00:00Z',
    assignments: [{ teamId: 't2', teamName: 'Team Beta', role: 'Support' }],
    reports: [],
  },
  {
    id: 'ir3',
    irNumber: 'IR-MYS-2026-00001',
    title: 'Heritage site maintenance audit',
    description: 'Audit of maintenance contracts for Mysuru palace vicinity.',
    status: 'Consolidated',
    ioName: 'Ops Admin',
    ioUserId: 'u-ops',
    createdAt: '2026-05-20T11:00:00Z',
    assignments: [
      { teamId: 't3', teamName: 'Team Gamma', role: 'Lead' },
      { teamId: 't1', teamName: 'Team Alpha', role: 'Review' },
    ],
    reports: [
      { teamName: 'Team Gamma', reportBody: 'Field inspection complete. Minor repairs needed on south wing fencing.', submittedAt: '2026-05-28T10:00:00Z' },
      { teamName: 'Team Alpha', reportBody: 'Consolidated report: Recommend phased repair over 90 days with budget estimate ₹12L.', submittedAt: '2026-06-02T16:00:00Z' },
    ],
  },
];

export const EARNINGS_SERIES = [
  { day: 'Mon', amount: 1420 },
  { day: 'Tue', amount: 1680 },
  { day: 'Wed', amount: 1890 },
  { day: 'Thu', amount: 1560 },
  { day: 'Fri', amount: 2100 },
  { day: 'Sat', amount: 2450 },
  { day: 'Sun', amount: 1980 },
];

function post(
  id: string,
  authorId: string,
  title: string,
  body: string,
  type: NewsPost['type'],
  status: NewsPost['status'],
  city: string,
  language: string,
  mediaUrl: string,
  mediaType: 'image' | 'video' | 'audio',
  thumbnailUrl?: string,
  durationSec?: number,
): NewsPost {
  const author = INITIAL_USERS.find(u => u.id === authorId)!;
  return {
    id,
    authorId,
    title,
    body,
    type,
    status,
    city,
    language,
    likesCount: type === 'Reel' ? Math.floor(Math.random() * 3000) + 1000 : Math.floor(Math.random() * 800) + 100,
    viewsCount: type === 'Reel' ? Math.floor(Math.random() * 100000) + 20000 : Math.floor(Math.random() * 30000) + 5000,
    durationSec,
    createdAt: new Date(Date.now() - Math.random() * 7 * 86400000).toISOString(),
    author: { id: author.id, displayName: author.displayName, avatarUrl: author.avatarUrl, isPremium: author.isPremium },
    media: [{
      id: `${id}-m`,
      type: mediaType === 'image' ? 'Image' : mediaType === 'video' ? 'Video' : 'Audio',
      url: mediaUrl,
      thumbnailUrl,
    }],
  };
}

export function findUserByEmail(email: string) {
  return INITIAL_USERS.find(u => u.email.toLowerCase() === email.toLowerCase());
}

export function nextIrNumber(cityCode = 'BLR', existing: Investigation[]) {
  const year = new Date().getFullYear();
  const prefix = `IR-${cityCode}-${year}-`;
  const max = existing
    .filter(i => i.irNumber.startsWith(prefix))
    .map(i => parseInt(i.irNumber.slice(prefix.length), 10))
    .reduce((a, b) => Math.max(a, b), 0);
  return `${prefix}${String(max + 1).padStart(5, '0')}`;
}
