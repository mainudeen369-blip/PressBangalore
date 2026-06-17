import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mic, Video, Image as ImageIcon, FileText, CheckCircle2, Clock, XCircle } from 'lucide-react';
import { useAuth } from '../lib/auth';
import { useDemo } from '../lib/demo-store';
import { AppShell } from '../components/Layout';
import { ReporterIdCard, AppointmentLetter } from '../components/ReporterIdCard';

const STATUS_ICON = {
  Approved: <CheckCircle2 className="text-green-400" size={20} />,
  Pending: <Clock className="text-yellow-400" size={20} />,
  Rejected: <XCircle className="text-red-400" size={20} />,
  Suspended: <XCircle className="text-orange-400" size={20} />,
};

export function ReporterPage() {
  const { user } = useAuth();
  const { registerReporter, createPost } = useDemo();
  const [tab, setTab] = useState<'dashboard' | 'post' | 'record'>('dashboard');

  if (!user) {
    return (
      <AppShell title="Reporter">
        <div className="px-4 py-12 text-center">
          <p className="text-[#a8a8a8]">Please <Link to="/login" className="text-sky-400">log in</Link> to access reporter tools.</p>
        </div>
      </AppShell>
    );
  }

  const profile = user.reporterProfile;

  return (
    <AppShell title="Reporter Hub">
      <div className="px-4">
        {!profile && <RegisterForm onSubmit={registerReporter} />}

        {profile && (
          <>
            <div className="card mb-4 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-[#a8a8a8]">Reporter status</p>
                  <p className="mt-1 flex items-center gap-2 text-xl font-bold">
                    {STATUS_ICON[profile.status]} {profile.status}
                  </p>
                </div>
                <div className="text-right text-xs text-[#a8a8a8]">
                  <p>{profile.area}</p>
                  <p>{profile.beat}</p>
                </div>
              </div>
              {profile.status === 'Rejected' && profile.rejectionReason && (
                <p className="mt-2 text-sm text-red-400">Reason: {profile.rejectionReason}</p>
              )}
            </div>

            {profile.status === 'Approved' && (
              <>
                <div className="mb-4 flex gap-2 overflow-x-auto">
                  {(['dashboard', 'post', 'record'] as const).map(t => (
                    <button key={t} type="button" onClick={() => setTab(t)}
                      className={`chip shrink-0 ${tab === t ? 'chip-active' : 'chip-inactive'}`}>
                      {t === 'dashboard' ? 'ID & Letter' : t === 'post' ? 'New post' : 'Record A/V'}
                    </button>
                  ))}
                </div>

                {tab === 'dashboard' && (
                  <div className="space-y-4">
                    <ReporterIdCard user={user} />
                    <AppointmentLetter user={user} />
                  </div>
                )}

                {tab === 'post' && <CreatePostForm onSubmit={createPost} />}
                {tab === 'record' && <RecordAVForm onSubmit={createPost} />}
              </>
            )}

            {profile.status === 'Pending' && (
              <div className="card p-6 text-center">
                <Clock size={40} className="mx-auto text-yellow-400" />
                <p className="mt-3 font-semibold">Awaiting admin approval</p>
                <p className="mt-1 text-sm text-[#a8a8a8]">An admin will review your application shortly. Log in as Super Admin to approve.</p>
                <Link to="/admin" className="mt-4 inline-block text-sm text-sky-400">Go to admin panel →</Link>
              </div>
            )}
          </>
        )}
      </div>
    </AppShell>
  );
}

function RegisterForm({ onSubmit }: { onSubmit: (d: { area: string; beat: string; languages: string; idDocumentUrl?: string }) => void }) {
  const [area, setArea] = useState('');
  const [beat, setBeat] = useState('');
  const [languages, setLanguages] = useState('en,kn');
  const [done, setDone] = useState(false);

  if (done) return <p className="py-8 text-center text-green-400">Application submitted! Status: Pending</p>;

  return (
    <form onSubmit={e => { e.preventDefault(); onSubmit({ area, beat, languages }); setDone(true); }} className="space-y-4">
      <h2 className="text-lg font-bold">Become a verified reporter</h2>
      <p className="text-sm text-[#a8a8a8]">Register with your beat area. Admin approval required before publishing.</p>
      <input value={area} onChange={e => setArea(e.target.value)} placeholder="Area (e.g. Koramangala)" required className="input" />
      <input value={beat} onChange={e => setBeat(e.target.value)} placeholder="Beat / zone" required className="input" />
      <input value={languages} onChange={e => setLanguages(e.target.value)} placeholder="Languages (en,kn)" className="input" />
      <label className="block">
        <span className="text-sm text-[#a8a8a8]">ID document (demo)</span>
        <div className="mt-2 flex h-24 items-center justify-center rounded-xl border border-dashed border-[#444] bg-[#1a1a1a] text-sm text-[#666]">
          <FileText size={20} className="mr-2" /> Tap to upload — simulated
        </div>
      </label>
      <button type="submit" className="btn-primary w-full">Submit application</button>
    </form>
  );
}

function CreatePostForm({ onSubmit }: {
  onSubmit: (d: { title: string; body: string; type: 'News' | 'Business' | 'Entertainment' | 'Professional' | 'Reel'; language: string; mediaUrl: string; mediaType: 'Image' | 'Video' | 'Audio' }) => void;
}) {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [type, setType] = useState<'News' | 'Business' | 'Entertainment' | 'Professional' | 'Reel'>('News');
  const [mediaType, setMediaType] = useState<'Image' | 'Video' | 'Audio'>('Image');
  const [done, setDone] = useState(false);

  const mediaUrls = {
    Image: 'https://picsum.photos/seed/newpost/800/600',
    Video: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
    Audio: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
  };

  if (done) return <p className="py-8 text-center text-green-400">Post submitted for approval!</p>;

  return (
    <form onSubmit={e => {
      e.preventDefault();
      onSubmit({ title, body, type, language: 'en', mediaUrl: mediaUrls[mediaType], mediaType });
      setDone(true);
    }} className="space-y-3">
      <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Headline" required className="input" />
      <textarea value={body} onChange={e => setBody(e.target.value)} placeholder="Story" required rows={4} className="input" />
      <select value={type} onChange={e => setType(e.target.value as typeof type)} className="input">
        <option value="News">News</option>
        <option value="Business">Business</option>
        <option value="Entertainment">Entertainment</option>
        <option value="Professional">Professional</option>
        <option value="Reel">Reel</option>
      </select>
      <div className="flex gap-2">
        {(['Image', 'Video', 'Audio'] as const).map(m => (
          <button key={m} type="button" onClick={() => setMediaType(m)}
            className={`flex flex-1 flex-col items-center gap-1 rounded-xl py-3 ${mediaType === m ? 'bg-white text-black' : 'bg-[#262626]'}`}>
            {m === 'Image' && <ImageIcon size={20} />}
            {m === 'Video' && <Video size={20} />}
            {m === 'Audio' && <Mic size={20} />}
            <span className="text-[10px]">{m}</span>
          </button>
        ))}
      </div>
      <button type="submit" className="btn-primary w-full">Submit for approval</button>
    </form>
  );
}

function RecordAVForm({ onSubmit }: { onSubmit: (d: { title: string; body: string; type: 'News'; language: string; mediaUrl: string; mediaType: 'Video' | 'Audio' }) => void }) {
  const [recording, setRecording] = useState(false);
  const [done, setDone] = useState(false);

  if (done) return <p className="py-8 text-center text-green-400">Recording saved & submitted!</p>;

  return (
    <div className="card p-6 text-center">
      <div className={`mx-auto flex h-32 w-32 items-center justify-center rounded-full ${recording ? 'bg-red-500/20 animate-pulse' : 'bg-[#262626]'}`}>
        <Mic size={48} className={recording ? 'text-red-400' : 'text-white'} />
      </div>
      <p className="mt-4 font-semibold">{recording ? 'Recording…' : 'Reporter A/V recording'}</p>
      <p className="mt-1 text-sm text-[#a8a8a8]">Simulated voice/video capture for field reports</p>
      <div className="mt-6 flex gap-3">
        <button type="button" onClick={() => setRecording(!recording)} className={`btn-ghost flex-1 ${recording ? 'border-red-500 text-red-400' : ''}`}>
          {recording ? 'Stop' : 'Start recording'}
        </button>
        <button type="button" onClick={() => {
          onSubmit({ title: 'Field recording', body: 'On-ground audio report from reporter.', type: 'News', language: 'en', mediaUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3', mediaType: 'Audio' });
          setDone(true);
        }} className="btn-primary flex-1">Save & submit</button>
      </div>
    </div>
  );
}
