import { useState } from 'react'

export default function SettingsPage() {
  const [temperature, setTemperature] = useState(0.2)
  const [topK, setTopK] = useState(5)

  return (
    <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-2xl shadow-black/20">
      <h1 className="text-2xl font-semibold text-white">Settings</h1>
      <div className="mt-6 space-y-6">
        <div>
          <label className="mb-2 block text-sm text-slate-300">Temperature</label>
          <input type="range" min="0" max="1" step="0.1" value={temperature} onChange={(event) => setTemperature(Number(event.target.value))} className="w-full" />
          <p className="mt-1 text-sm text-slate-400">Current: {temperature}</p>
        </div>
        <div>
          <label className="mb-2 block text-sm text-slate-300">Top K results</label>
          <input type="range" min="1" max="10" step="1" value={topK} onChange={(event) => setTopK(Number(event.target.value))} className="w-full" />
          <p className="mt-1 text-sm text-slate-400">Current: {topK}</p>
        </div>
      </div>
    </div>
  )
}
