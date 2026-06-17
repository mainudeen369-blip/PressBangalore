import { useParams } from 'react-router-dom';
import { Heart, Share2, Volume2 } from 'lucide-react';
import { useDemo } from '../lib/demo-store';
import { AppShell } from '../components/Layout';
import { PageBackHeader } from '../components/BackButton';
import { useBackNavigation } from '../lib/back-navigation';

export function PostDetailPage() {
  const { id } = useParams();
  const { getPost, toggleLike, isLiked } = useDemo();
  const { goBack } = useBackNavigation();
  const post = id ? getPost(id) : undefined;

  if (!post) {
    return (
      <AppShell>
        <div className="px-4 py-16 text-center text-[#a8a8a8]">
          <p>Post not found</p>
          <button type="button" onClick={goBack} className="mt-4 text-sky-400">Go back</button>
        </div>
      </AppShell>
    );
  }

  const media = post.media[0];
  const liked = isLiked(post.id);

  return (
    <AppShell showHeader={false}>
      <PageBackHeader title="Post" />

      <div className="px-4 py-4">
        <div className="mb-4 flex items-center gap-3">
          <img src={post.author.avatarUrl ?? `https://i.pravatar.cc/150?u=${post.author.id}`} alt="" className="h-10 w-10 rounded-full object-cover" />
          <div>
            <p className="font-semibold">{post.author.displayName}</p>
            <p className="text-xs text-[#a8a8a8]">{post.city} · {new Date(post.createdAt).toLocaleDateString()}</p>
          </div>
        </div>

        {media?.type === 'Image' && <img src={media.url} alt="" className="w-full rounded-2xl" />}
        {media?.type === 'Video' && <video src={media.url} poster={media.thumbnailUrl} controls className="w-full rounded-2xl" />}
        {media?.type === 'Audio' && (
          <div className="card flex items-center gap-4 p-6">
            <Volume2 size={32} className="text-[#dd2a7b]" />
            <audio src={media.url} controls className="flex-1" />
          </div>
        )}

        <div className="mt-4 flex items-center gap-4">
          <button type="button" onClick={() => toggleLike(post.id)} className={liked ? 'text-[#ed4956]' : 'text-white'}>
            <Heart size={28} fill={liked ? 'currentColor' : 'none'} />
          </button>
          <button type="button" className="text-white"><Share2 size={28} /></button>
          <span className="text-sm font-semibold">{post.likesCount.toLocaleString()} likes</span>
        </div>

        <h1 className="mt-4 text-xl font-bold">{post.title}</h1>
        <p className="mt-3 leading-relaxed text-[#d4d4d4]">{post.body}</p>
        <p className="mt-4 text-xs text-[#666]">{post.viewsCount.toLocaleString()} views · {post.type} · {post.language.toUpperCase()}</p>
      </div>
    </AppShell>
  );
}
