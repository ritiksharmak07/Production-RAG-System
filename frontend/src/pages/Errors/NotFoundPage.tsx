import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center rounded-3xl border border-white/10 bg-slate-900/70 p-10 text-center shadow-2xl shadow-black/20">
      <h1 className="text-4xl font-semibold text-white">404</h1>
      <p className="mt-3 text-slate-400">The page you are looking for could not be found.</p>
      <Link to="/" className="mt-6 rounded-2xl bg-brand-500 px-4 py-3 font-medium text-white transition hover:bg-brand-700">Back to home</Link>
    </div>
  )
}
