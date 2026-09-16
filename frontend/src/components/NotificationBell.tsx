import { CheckCircle, AlertTriangle } from 'lucide-react'
import type { Notification } from '../hooks/useNotifications'

export default function NotificationBell({ notification }: { notification: Notification }) {
  return (
    <div className={`flex items-center gap-2 rounded-2xl px-3 py-2 text-sm ${notification.type === 'success' ? 'bg-emerald-500/10 text-emerald-200' : notification.type === 'error' ? 'bg-rose-500/10 text-rose-200' : 'bg-slate-800/80 text-slate-300'}`}>
      {notification.type === 'success' ? <CheckCircle size={16} /> : notification.type === 'error' ? <AlertTriangle size={16} /> : <span className="h-4 w-4 rounded-full bg-slate-400" />}
      <span>{notification.message}</span>
    </div>
  )
}
