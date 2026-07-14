import { Link, NavLink } from 'react-router-dom'
import { Bot, FileUp, Search, Settings, Sparkles } from 'lucide-react'

const navItems = [
  { to: '/', label: 'Home', icon: Sparkles },
  { to: '/chat', label: 'Chat', icon: Bot },
  { to: '/search', label: 'Search', icon: Search },
  { to: '/upload', label: 'Upload', icon: FileUp },
  { to: '/settings', label: 'Settings', icon: Settings },
]

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-transparent text-slate-100">
      <div className="mx-auto flex max-w-7xl flex-col lg:flex-row">
        <aside className="w-full border-b border-white/10 bg-slate-950/70 p-4 backdrop-blur lg:min-h-screen lg:w-72 lg:border-b-0 lg:border-r">
          <Link to="/" className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm font-semibold tracking-wide text-white">
            <div className="rounded-xl bg-brand-500/20 p-2 text-brand-500">
              <Sparkles size={18} />
            </div>
            RAG Studio
          </Link>
          <nav className="mt-6 space-y-2">
            {navItems.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-2xl px-3 py-2.5 text-sm transition ${isActive ? 'bg-white/10 text-white' : 'text-slate-400 hover:bg-white/5 hover:text-white'}`
                }
              >
                <Icon size={18} />
                {label}
              </NavLink>
            ))}
          </nav>
        </aside>
        <main className="flex-1 p-4 sm:p-6 lg:p-8">{children}</main>
      </div>
    </div>
  )
}
