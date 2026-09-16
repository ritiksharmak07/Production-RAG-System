import NotificationBell from './NotificationBell'
import type { Notification } from '../hooks/useNotifications'

export default function NotificationPanel({ notifications }: { notifications: Notification[] }) {
  if (!notifications.length) return null

  return (
    <div className="fixed bottom-4 right-4 z-50 space-y-2">
      {notifications.map((notification) => (
        <NotificationBell key={notification.id} notification={notification} />
      ))}
    </div>
  )
}
