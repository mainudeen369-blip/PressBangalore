import { ArrowLeft } from 'lucide-react';
import { useBackNavigation } from '../lib/back-navigation';

export function BackButton({ className = '' }: { className?: string }) {
  const { goBack } = useBackNavigation();

  return (
    <button
      type="button"
      onClick={goBack}
      aria-label="Go back"
      className={`flex h-10 w-10 items-center justify-center rounded-full text-white transition active:bg-white/10 ${className}`}
    >
      <ArrowLeft size={24} strokeWidth={2} />
    </button>
  );
}

export function PageBackHeader({
  title,
  className = '',
  dark = true,
}: {
  title: string;
  className?: string;
  dark?: boolean;
}) {
  return (
    <header
      className={`sticky top-0 z-50 flex items-center gap-2 border-b px-2 py-2 backdrop-blur-xl safe-top ${
        dark ? 'border-[#262626]/80 bg-black/90' : 'border-gray-200 bg-white/90'
      } ${className}`}
    >
      <BackButton />
      <h1 className={`flex-1 text-center text-base font-semibold pr-10 ${dark ? 'text-white' : 'text-black'}`}>
        {title}
      </h1>
    </header>
  );
}
