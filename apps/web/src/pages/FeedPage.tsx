import { useState } from 'react';
import { useDemo } from '../lib/demo-store';
import { AppShell } from '../components/Layout';
import { StoriesBar } from '../components/StoriesBar';
import { PostCard, AdBanner } from '../components/PostCard';
import { CITIES, LANGUAGES } from '../mock/data';

export function FeedPage() {
  const { getFeed, ads } = useDemo();
  const [city, setCity] = useState('Bangalore');
  const [language, setLanguage] = useState<string | null>(null);

  const feed = getFeed(city, language);
  const topAd = ads.find(a => a.isActive && a.slot === 'FeedTop' && (!a.targetCity || a.targetCity === city));
  const inlineAd = ads.find(a => a.isActive && a.slot === 'FeedInline' && (!a.targetCity || a.targetCity === city));

  return (
    <AppShell>
      <StoriesBar />

      <div className="mb-4 flex flex-wrap gap-2 px-4">
        {CITIES.map(c => (
          <button key={c} type="button" onClick={() => setCity(c)}
            className={`chip ${city === c ? 'chip-active' : 'chip-inactive'}`}>{c}</button>
        ))}
      </div>
      <div className="mb-4 flex flex-wrap gap-2 px-4">
        <button type="button" onClick={() => setLanguage(null)}
          className={`chip ${language === null ? 'bg-gradient-to-r from-[#f58529] to-[#dd2a7b] text-white' : 'chip-inactive'}`}>All</button>
        {LANGUAGES.map(l => (
          <button key={l.code} type="button" onClick={() => setLanguage(l.code)}
            className={`chip ${language === l.code ? 'bg-gradient-to-r from-[#f58529] to-[#dd2a7b] text-white' : 'chip-inactive'}`}>{l.label}</button>
        ))}
      </div>

      <div className="space-y-5 px-4 pb-4">
        {topAd && <AdBanner title={topAd.title} imageUrl={topAd.imageUrl} linkUrl={topAd.linkUrl} />}
        {feed.map((post, i) => (
          <div key={post.id}>
            <PostCard post={post} />
            {i === 1 && inlineAd && <div className="mt-5"><AdBanner title={inlineAd.title} imageUrl={inlineAd.imageUrl} /></div>}
          </div>
        ))}
        {feed.length === 0 && (
          <p className="py-16 text-center text-[#a8a8a8]">No posts for this filter. Try another city or language.</p>
        )}
      </div>
    </AppShell>
  );
}
