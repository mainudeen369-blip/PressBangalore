import { STORIES } from '../mock/data';

export function StoriesBar() {
  return (
    <div className="flex gap-3 overflow-x-auto px-4 py-3 scrollbar-none">
      <button type="button" className="flex shrink-0 flex-col items-center gap-1">
        <div className="flex h-[68px] w-[68px] items-center justify-center rounded-full border-2 border-dashed border-[#444] bg-[#1a1a1a] text-2xl">+</div>
        <span className="max-w-[64px] truncate text-[11px]">Your story</span>
      </button>
      {STORIES.map(s => (
        <button key={s.id} type="button" className="flex shrink-0 flex-col items-center gap-1">
          <div className={s.hasNew ? 'story-ring' : 'story-ring-seen'}>
            <img src={s.avatar} alt="" className="h-16 w-16 rounded-full border-2 border-black object-cover" />
          </div>
          <span className="max-w-[64px] truncate text-[11px]">{s.name}</span>
        </button>
      ))}
    </div>
  );
}
