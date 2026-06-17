import { useState, useRef, useCallback } from 'react';
import { Heart, MessageCircle, Share2, Music2, ChevronUp, ChevronDown } from 'lucide-react';
import { useDemo } from '../lib/demo-store';
import { usePageBackHandler } from '../lib/back-navigation';
import { BackButton } from '../components/BackButton';
import { BottomNav } from '../components/Layout';

export function ReelsPage() {
  const { getReels, toggleLike, isLiked } = useDemo();
  const reels = getReels();
  const [index, setIndex] = useState(0);
  const touchStart = useRef(0);
  const indexRef = useRef(0);
  indexRef.current = index;

  const go = (dir: 1 | -1) => {
    const next = index + dir;
    if (next >= 0 && next < reels.length) setIndex(next);
  };

  const handlePageBack = useCallback(() => {
    if (indexRef.current > 0) {
      setIndex(i => i - 1);
      return true;
    }
    return false;
  }, []);

  usePageBackHandler(handlePageBack, [handlePageBack]);

  const current = reels[index];
  if (!current) {
    return (
      <div className="flex h-screen flex-col bg-black">
        <PageBackHeader />
        <div className="flex flex-1 items-center justify-center text-[#a8a8a8]">No reels available</div>
        <BottomNav />
      </div>
    );
  }

  const media = current.media[0];
  const liked = isLiked(current.id);

  return (
    <div className="relative h-screen overflow-hidden bg-black pb-[72px]">
      <div
        className="absolute inset-0 bottom-[72px]"
        onTouchStart={e => { touchStart.current = e.touches[0].clientY; }}
        onTouchEnd={e => {
          const diff = touchStart.current - e.changedTouches[0].clientY;
          if (diff > 50) go(1);
          if (diff < -50) go(-1);
        }}
      >
        <video key={current.id} src={media?.url} poster={media?.thumbnailUrl} className="h-full w-full object-cover" autoPlay loop muted playsInline />

        <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/90 via-transparent to-black/40" />

        <div className="absolute top-0 left-0 right-0 z-20 flex items-center justify-between px-2 pt-safe">
          <BackButton />
          <p className="gradient-text text-lg font-bold">Reels</p>
          <div className="w-10" />
        </div>

        <div className="absolute right-3 bottom-8 z-10 flex flex-col items-center gap-6">
          <button type="button" onClick={() => toggleLike(current.id)} className={`flex flex-col items-center gap-1 ${liked ? 'text-[#ed4956]' : 'text-white'}`}>
            <Heart size={30} fill={liked ? 'currentColor' : 'none'} />
            <span className="text-xs font-semibold">{current.likesCount.toLocaleString()}</span>
          </button>
          <button type="button" className="flex flex-col items-center gap-1 text-white">
            <MessageCircle size={30} />
            <span className="text-xs">248</span>
          </button>
          <button type="button" className="text-white"><Share2 size={28} /></button>
        </div>

        <div className="absolute bottom-8 left-4 right-16 z-10">
          <p className="flex items-center gap-2 font-bold">
            {current.author.displayName}
            <span className="rounded bg-white/20 px-1.5 py-0.5 text-[10px]">{current.type}</span>
          </p>
          <p className="mt-1 text-sm font-medium">{current.title}</p>
          <p className="mt-1 line-clamp-2 text-xs text-[#d4d4d4]">{current.body}</p>
          <p className="mt-2 flex items-center gap-2 text-xs text-[#a8a8a8]">
            <Music2 size={14} /> Original audio · {current.viewsCount.toLocaleString()} views
          </p>
        </div>

        {index > 0 && (
          <button type="button" onClick={() => go(-1)} className="absolute top-1/2 left-1/2 z-20 -translate-x-1/2 -translate-y-16 text-white/50" aria-label="Previous reel">
            <ChevronUp size={32} />
          </button>
        )}
        {index < reels.length - 1 && (
          <button type="button" onClick={() => go(1)} className="absolute bottom-24 left-1/2 z-20 -translate-x-1/2 text-white/50" aria-label="Next reel">
            <ChevronDown size={32} />
          </button>
        )}

        <div className="absolute right-2 top-1/2 z-10 flex -translate-y-1/2 flex-col gap-1">
          {reels.map((_, i) => (
            <div key={i} className={`h-6 w-0.5 rounded-full transition ${i === index ? 'bg-white' : 'bg-white/30'}`} />
          ))}
        </div>
      </div>

      <BottomNav />
    </div>
  );
}

function PageBackHeader() {
  return (
    <div className="flex items-center gap-2 border-b border-[#262626] px-2 py-3">
      <BackButton />
      <span className="gradient-text text-lg font-bold">Reels</span>
    </div>
  );
}
