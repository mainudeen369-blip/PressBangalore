import { QrCode, MapPin, Calendar, Shield } from 'lucide-react';
import type { User } from '../types';

export function ReporterIdCard({ user }: { user: User }) {
  const profile = user.reporterProfile;
  if (!profile || profile.status !== 'Approved') return null;

  return (
    <div className="overflow-hidden rounded-2xl border border-[#333] bg-gradient-to-br from-[#1a1a2e] via-[#16213e] to-[#0f3460] p-5 shadow-xl">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#dd2a7b]">PressBangalore</p>
          <p className="mt-0.5 text-xs text-[#a8a8a8]">Accredited Reporter</p>
        </div>
        <Shield className="text-sky-400" size={28} />
      </div>

      <div className="mt-4 flex gap-4">
        <img
          src={user.avatarUrl ?? `https://i.pravatar.cc/150?u=${user.id}`}
          alt=""
          className="h-20 w-20 rounded-xl border-2 border-white/20 object-cover"
        />
        <div className="flex-1">
          <h3 className="text-lg font-bold">{user.displayName}</h3>
          <p className="font-mono text-xs text-sky-300">{profile.pressId ?? 'PB-REP-PENDING'}</p>
          <div className="mt-2 space-y-1 text-xs text-[#ccc]">
            <p className="flex items-center gap-1.5"><MapPin size={12} /> {profile.area}, {profile.beat}</p>
            <p className="flex items-center gap-1.5"><Calendar size={12} /> Since {profile.appointedDate ?? '2026'}</p>
          </div>
        </div>
      </div>

      <div className="mt-4 flex items-center justify-between rounded-xl bg-black/30 p-3">
        <div className="text-[10px] text-[#a8a8a8]">
          <p>Languages: {profile.languages}</p>
          <p className="mt-1">City: {user.city}</p>
        </div>
        <QrCode size={40} className="text-white/60" />
      </div>
    </div>
  );
}

export function AppointmentLetter({ user }: { user: User }) {
  const profile = user.reporterProfile;
  if (!profile?.appointmentLetterUrl) return null;

  return (
    <div className="card overflow-hidden">
      <div className="border-b border-[#262626] px-4 py-3">
        <p className="text-sm font-semibold">Appointment Letter</p>
        <p className="text-xs text-[#a8a8a8]">Official area assignment — {profile.area}</p>
      </div>
      <img src={profile.appointmentLetterUrl} alt="Appointment letter" className="w-full object-cover" />
      <div className="p-3">
        <button type="button" className="btn-ghost w-full text-sm">Download PDF (demo)</button>
      </div>
    </div>
  );
}
