import { Link } from 'react-router-dom';
import { Heart, MessageCircle, Share2, BadgeCheck, Bookmark, Play, Volume2 } from 'lucide-react';
import { useDemo } from '../lib/demo-store';
import type { NewsPost } from '../types';

export function PostCard({ post }: { post: NewsPost }) {
  const { toggleLike, isLiked } = useDemo();
  const media = post.media[0];
  const liked = isLiked(post.id);

  return (
    <article className="card overflow-hidden">
      <div className="flex items-center gap-3 p-3">
        <Link to="/profile" className="flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-full bg-gradient-to-br from-[#f58529] to-[#8134af]">
          {post.author.avatarUrl
            ? <img src={post.author.avatarUrl} alt="" className="h-full w-full object-cover" />
            : <span className="text-sm font-bold">{post.author.displayName[0]}</span>}
        </Link>
        <div className="min-w-0 flex-1">
          <p className="flex items-center gap-1 truncate text-sm font-semibold">
            {post.author.displayName}
            {post.author.isPremium && <BadgeCheck size={14} className="shrink-0 text-sky-400" />}
          </p>
          <p className="truncate text-xs text-[#a8a8a8]">{post.city} · {post.type} · {post.language.toUpperCase()}</p>
        </div>
        <span className="rounded-full bg-[#262626] px-2 py-0.5 text-[10px] uppercase tracking-wide text-[#a8a8a8]">{post.type}</span>
      </div>

      {media?.type === 'Image' && (
        <Link to={`/post/${post.id}`}>
          <img src={media.url} alt={post.title} className="aspect-[4/5] w-full object-cover" loading="lazy" />
        </Link>
      )}
      {media?.type === 'Video' && (
        <Link to={`/post/${post.id}`} className="relative block">
          <img src={media.thumbnailUrl ?? media.url} alt="" className="aspect-[4/5] w-full object-cover" />
          <div className="absolute inset-0 flex items-center justify-center bg-black/20">
            <div className="flex h-14 w-14 items-center justify-center rounded-full bg-white/90 text-black"><Play size={28} fill="currentColor" /></div>
          </div>
        </Link>
      )}
      {media?.type === 'Audio' && (
        <Link to={`/post/${post.id}`} className="mx-3 mb-2 flex items-center gap-3 rounded-xl bg-[#1a1a1a] p-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br from-[#f58529] to-[#dd2a7b]"><Volume2 size={22} /></div>
          <div className="flex-1">
            <p className="text-sm font-medium">Audio report</p>
            <p className="text-xs text-[#a8a8a8]">Tap to listen</p>
          </div>
        </Link>
      )}

      <div className="flex items-center justify-between px-3 py-2.5">
        <div className="flex items-center gap-4">
          <button type="button" onClick={() => toggleLike(post.id)} className={`flex items-center gap-1.5 transition ${liked ? 'text-[#ed4956]' : 'text-white'}`}>
            <Heart size={24} strokeWidth={1.8} fill={liked ? 'currentColor' : 'none'} />
            <span className="text-sm font-semibold">{post.likesCount.toLocaleString()}</span>
          </button>
          <button type="button" className="text-white"><MessageCircle size={24} strokeWidth={1.8} /></button>
          <button type="button" className="text-white"><Share2 size={24} strokeWidth={1.8} /></button>
        </div>
        <button type="button" className="text-white"><Bookmark size={24} strokeWidth={1.8} /></button>
      </div>

      <div className="px-3 pb-4">
        <Link to={`/post/${post.id}`}>
          <p className="text-sm font-semibold">{post.title}</p>
          <p className="mt-1 line-clamp-2 text-sm text-[#d4d4d4]">{post.body}</p>
        </Link>
        <p className="mt-2 text-[11px] text-[#666]">{post.viewsCount.toLocaleString()} views</p>
      </div>
    </article>
  );
}

export function AdBanner({ title, imageUrl }: { title: string; imageUrl: string; linkUrl?: string }) {
  return (
    <div className="card overflow-hidden">
      <div className="flex items-center justify-between bg-[#1a1a1a] px-3 py-1.5">
        <span className="text-[10px] font-semibold uppercase tracking-widest text-[#a8a8a8]">Sponsored</span>
        <span className="text-[10px] text-[#666]">Ad</span>
      </div>
      <img src={imageUrl} alt={title} className="h-32 w-full object-cover" loading="lazy" />
      <p className="p-3 text-sm font-semibold">{title}</p>
    </div>
  );
}
