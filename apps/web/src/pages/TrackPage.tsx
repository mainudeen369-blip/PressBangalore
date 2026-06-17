import { useState } from 'react';
import { useDemo } from '../lib/demo-store';
import { AppShell } from '../components/Layout';

const STATUS_STEPS = ['Open', 'Assigned', 'InProgress', 'Consolidated', 'Closed'] as const;

export function TrackPage() {
  const { trackIr, investigations } = useDemo();
  const [irNumber, setIrNumber] = useState('IR-BLR-2026-00001');
  const [result, setResult] = useState<ReturnType<typeof trackIr>>(undefined);
  const [searched, setSearched] = useState(false);

  const search = () => {
    setResult(trackIr(irNumber));
    setSearched(true);
  };

  return (
    <AppShell title="Track IR">
      <div className="px-4">
        <p className="mb-4 text-sm text-[#a8a8a8]">Enter your Investigation Report number to track status publicly.</p>

        <form onSubmit={e => { e.preventDefault(); search(); }} className="mb-4 flex gap-2">
          <input value={irNumber} onChange={e => setIrNumber(e.target.value)} placeholder="IR-BLR-2026-00001"
            className="input flex-1 font-mono text-sm" />
          <button type="submit" className="btn-primary shrink-0 px-5">Track</button>
        </form>

        <div className="mb-6 flex flex-wrap gap-2">
          {investigations.slice(0, 3).map(ir => (
            <button key={ir.id} type="button" onClick={() => { setIrNumber(ir.irNumber); setResult(ir); setSearched(true); }}
              className="rounded-full bg-[#262626] px-3 py-1 font-mono text-[10px]">{ir.irNumber}</button>
          ))}
        </div>

        {searched && !result && (
          <p className="py-12 text-center text-[#a8a8a8]">No investigation found for <span className="font-mono text-white">{irNumber}</span></p>
        )}

        {result && (
          <div className="space-y-4">
            <div className="card p-5">
              <p className="font-mono text-lg text-sky-400">{result.irNumber}</p>
              <h2 className="mt-1 text-xl font-bold">{result.title}</h2>
              <p className="mt-3 text-sm leading-relaxed text-[#d4d4d4]">{result.description}</p>
              {result.ioName && <p className="mt-3 text-sm">Investigation Officer: <span className="font-semibold text-white">{result.ioName}</span></p>}
            </div>

            <div className="card p-4">
              <p className="mb-4 text-sm font-semibold">Status timeline</p>
              <div className="relative">
                <div className="absolute left-3 top-2 bottom-2 w-0.5 bg-[#333]" />
                {STATUS_STEPS.map((step, i) => {
                  const current = STATUS_STEPS.indexOf(result.status as typeof STATUS_STEPS[number]);
                  const done = i <= current;
                  return (
                    <div key={step} className="relative mb-4 flex items-center gap-4 pl-8">
                      <div className={`absolute left-1.5 h-4 w-4 rounded-full border-2 ${done ? 'border-green-400 bg-green-400' : 'border-[#444] bg-black'}`} />
                      <div>
                        <p className={`text-sm font-medium ${done ? 'text-white' : 'text-[#666]'}`}>{step}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {result.assignments.length > 0 && (
              <div className="card p-4">
                <p className="mb-2 font-semibold">Assigned teams</p>
                {result.assignments.map((a, i) => (
                  <div key={i} className="flex justify-between text-sm">
                    <span>{a.teamName}</span>
                    <span className="text-[#a8a8a8]">{a.role}</span>
                  </div>
                ))}
              </div>
            )}

            {result.reports.length > 0 && (
              <div className="card p-4">
                <p className="mb-3 font-semibold">Team reports & consolidation</p>
                {result.reports.map((r, i) => (
                  <div key={i} className="mb-3 rounded-xl bg-[#1a1a1a] p-3 last:mb-0">
                    <p className="text-xs font-semibold text-sky-400">{r.teamName}</p>
                    <p className="mt-1 text-sm">{r.reportBody}</p>
                    <p className="mt-1 text-[10px] text-[#666]">{new Date(r.submittedAt).toLocaleDateString()}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}
