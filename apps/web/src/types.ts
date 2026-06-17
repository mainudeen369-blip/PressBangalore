export type UserRole = 'Consumer' | 'Premium' | 'Reporter' | 'SubAdmin' | 'Admin' | 'SuperAdmin';

export interface ReporterProfile {
  id: string;
  area: string;
  beat: string;
  languages: string;
  status: 'Pending' | 'Approved' | 'Rejected' | 'Suspended';
  idDocumentUrl?: string;
  appointmentLetterUrl?: string;
  appointedDate?: string;
  pressId?: string;
  rejectionReason?: string;
}

export interface User {
  id: string;
  email: string;
  displayName: string;
  avatarUrl?: string;
  role: UserRole;
  isPremium: boolean;
  languagePref: string;
  city: string;
  followers: number;
  following: number;
  earnings: number;
  postsCount: number;
  reporterProfile?: ReporterProfile;
}

export interface PostMedia {
  id: string;
  type: 'Image' | 'Video' | 'Audio';
  url: string;
  thumbnailUrl?: string;
}

export interface NewsPost {
  id: string;
  authorId: string;
  title: string;
  body: string;
  type: 'News' | 'Reel' | 'Business' | 'Entertainment' | 'Professional';
  status: 'Draft' | 'PendingApproval' | 'Published' | 'Rejected';
  city: string;
  language: string;
  likesCount: number;
  viewsCount: number;
  durationSec?: number;
  createdAt: string;
  author: { id: string; displayName: string; avatarUrl?: string; isPremium: boolean };
  media: PostMedia[];
}

export interface Advertisement {
  id: string;
  title: string;
  imageUrl: string;
  linkUrl: string;
  slot: 'FeedTop' | 'FeedInline' | 'Reels';
  targetCity: string | null;
  isActive: boolean;
}

export interface Team {
  id: string;
  name: string;
  region: string;
  members: string[];
}

export interface Investigation {
  id: string;
  irNumber: string;
  title: string;
  description: string;
  status: 'Open' | 'Assigned' | 'InProgress' | 'Consolidated' | 'Closed';
  ioName?: string;
  ioUserId?: string;
  createdAt: string;
  assignments: { teamId: string; teamName: string; role: string }[];
  reports: { teamName: string; reportBody: string; submittedAt: string }[];
}

export interface DashboardStats {
  totalUsers: number;
  pendingReporters: number;
  pendingPosts: number;
  publishedPosts: number;
  openInvestigations: number;
}
